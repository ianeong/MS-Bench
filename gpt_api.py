import os
import re
import json
import base64
from openai import OpenAI

client = OpenAI(
    api_key = 'YOUR_API_KEY' #TODO: 替换为你自己的 openai_api_key
)


def encode_image_to_base64(image_path):
    """将图像转换为base64编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_question_with_gpt4(question):
    """调用 LMM 处理问题"""
    try:

        image_path = question.split("<img='")[1].split("'>")[0]  
        image_paths = []
        image_paths.append(image_path)
        images = [encode_image_to_base64(img) for img in image_paths]

        question = re.sub(r"<img='[^']+'>", "", question).strip()
        
        content = [{"type": "text", "text": question}] + [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in images
        ]

        response = client.chat.completions.create(
            model="gpt-4o", #TODO: 可以替换为其他任意模型
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing question: {question}, image: {image_paths}. Error: {str(e)}")
        return ""

def process_json_file(input_json_path, output_json_path):
    with open(input_json_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    results = []

    for record in data:
        no_ = record.get("No") # 获取问题 ID
        question = record.get("question", "") # 获取问题提示

        # 调用 gpt-4 处理问题
        response = process_question_with_gpt4(question)

        # 保存结果
        results.append({
            "No": record.get("No"),
            "question": question,
            "answer": response,
        })

    # 将结果写入输出文件
    with open(output_json_path, "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_json_path = "INPUT_JSON_PATH"     #TODO: input_json_path 替换为想要执行的任务的 json 文件路径
    output_json_path = "OUTPUT_JSON_PATH"   #TODO: output_json_path 替换为输出的 json 文件路径
    process_json_file(input_json_path, output_json_path)
    print(f"Processing complete. Results saved to {output_json_path}.")


