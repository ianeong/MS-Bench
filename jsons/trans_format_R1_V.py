import json
import re

def extract_image_path(question):
    """
    从 question 字段中提取 image_path。
    假设图片路径位于 <img='...'> 标签内。
    """
    match = re.search(r"<img='([^']+)'>", question)
    return match.group(1) if match else None

def process_json_file(input_file, output_file):
    """
    读取 JSON 文件，提取所需字段，并写入 JSONL 文件。
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for item in data:
            image_path = extract_image_path(item.get('question', ''))
            question = re.sub(r"<img='[^']+'>", '', item.get('question', '')).strip()
            ground_truth = item.get('answer', '')

            if image_path and question and ground_truth:
                new_item = {
                    'image_path': image_path,
                    'question': question,
                    'ground_truth': ground_truth
                }
                outfile.write(json.dumps(new_item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    input_file = 'count_average.json'   # 输入的 JSON 文件名
    output_file = 'count_average_r1_v.jsonl'  # 输出的 JSONL 文件名
    process_json_file(input_file, output_file)
    print(f'数据已成功写入 {output_file}')
