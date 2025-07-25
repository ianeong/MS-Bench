"""
任务：使用GPT-4o模型进行壁画图片描述
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

    try:
        question += ""

        response = client.chat.completions.create(
            model=model_name,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        {"type": "text", "text": question},
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

        question_text = re.sub(r"<img=[^']+>", "", question).strip()

        response = process_question_with_gpt4(question_text, image_path, model_name)

        results.append({
            "No": record.get("No"),
            "question": question,
            "answer": response,
        })
        print(f"No: {record.get("No")}; answer: {response}")
        # print(record.get("No"))

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

    input_json_path = "../../jsons/image_caption.json"  # input json的路径
    output_json_path = f"{folder_path}/image_caption_{model}.json"  # output json 的路径

    process_json_file(input_json_path, output_json_path, model_name)
    print(f"Processing complete. Results saved to {output_json_path}.")
