"""
任务：使用GPT-4o模型处理年代断定问题，判断给定图片的年代，并有知识增强的帮助
"""
import os
import re
import json
import base64
from openai import OpenAI
import openai
import requests
import sys
sys.path.append(os.path.abspath('../../'))
from load_config import load_config
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# 读取api的配置文件
# 获取当前工作目录的路径
current_dir = os.getcwd()
# 获取当前目录的名称
dir_name = os.path.basename(current_dir)
# 读取api的配置文件
config = load_config(f"../../api/{dir_name}.json")

# TODO：根据调用接口和api修改
client = OpenAI(
    api_key=config["api_key"],
)


def encode_image_to_base64(image_path):
    """将图像转换为base64编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(10),
       retry=retry_if_exception_type(Exception))
def process_question_with_gpt4(question, image_path, model_name):
    base64_image = encode_image_to_base64(image_path)
    # TODO: 修改一下图片的绝对路径
    img_wj = "../../datas/date_determination/date_determination_93.png"
    img_t = "../../datas/date_determination/date_determination_1.png"
    img_w = "../../datas/date_determination/date_determination_239.png"
    img_y = "../../datas/date_determination/date_determination_188.png"
    wj = encode_image_to_base64(img_wj)
    tang = encode_image_to_base64(img_t)
    wu = encode_image_to_base64(img_w)
    yuan = encode_image_to_base64(img_y)
    prompt = "根据上述信息，请推理判断下图5:<image>的是属于哪个时期的敦煌壁画？只在“魏晋南北朝”“唐代”“五代”“元代”中选择一个最接近的答案输出。不用输出原因。"
    prompt += "请直接输出答案。格式为“年代”，例如“年代: 元代”。"
    try:
        response = client.chat.completions.create(
            model=model_name,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "这里有几张不同时期的敦煌壁画。图1的年代是【魏晋南北朝】："},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{wj}"}},
                        {"type": "text", "text": "\n图2的年代是【唐代】："},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{tang}"}},
                        {"type": "text", "text": "\n图3的年代是【五代】："},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{wu}"}},
                        {"type": "text", "text": "\n图4的年代是【元代】："},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{yuan}"}},
                        {"type": "text",
                         "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing question: {question}, image: {image_path}. Error: {str(e)}")
        raise e


def process_json_file(input_json_path, output_json_path, model_name):
    with open(input_json_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    results = []

    for record in data:
        question = record.get("question", "")
        image_match = re.search(r"<img='([^']+)'>", question)

        if not image_match:
            print(f"No image found in question: {question}")
            continue

        image_path = image_match.group(1)
        # TODO: 加一下图片的绝对路径
        image_path = f"../../" + image_path

        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue

        question_text = re.sub(r"<img='[^']+'>", "", question).strip()

        response = process_question_with_gpt4(question_text, image_path, model_name)

        results.append({
            "No": record.get("No"),
            "question": question,
            "answer": response,
        })
        # print(f"No: {record.get("No")}; answer: {response}")
        print(record.get("No"))

    with open(output_json_path, "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # TODO: 修改model名称
    model_name = config["model_name"]
    model = model_name.split("/")[-1]

    # 如果output目录下不存在对应模型目录，创建目录
    folder_path = f"../../output/{model}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

    input_json_path = "../../jsons/date_determination.json"  # input json的路径
    output_json_path = f"{folder_path}/date_determination_{model}_know.json"  # output json 的路径
    process_json_file(input_json_path, output_json_path, model_name)
    print(f"Processing complete. Results saved to {output_json_path}.")


