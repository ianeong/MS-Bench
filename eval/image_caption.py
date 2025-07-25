import nltk
import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import jieba
import sys
import os
sys.path.append(os.path.abspath('../'))
from load_config import load_config

def calculate_bleu(reference, candidate):
    """
    计算候选文本相对于参考文本的 BLEU Score（适用于中文）。
    :param reference: 参考文本（字符串）
    :param candidate: 候选文本（字符串）
    :return: BLEU Score（浮点数）
    """
    # 使用 jieba 进行中文分词
    reference_tokens = [list(jieba.cut(reference))]
    candidate_tokens = list(jieba.cut(candidate))

    # 计算 BLEU Score
    smoothie = SmoothingFunction().method1  # 平滑处理
    score = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=smoothie)

    return score


def process_json_files(file1_path, file2_path, output_file):
    # 读取两个JSON文件
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    # 初始化输出字典
    output_data = []
    total_score = 0.0
    total = 0

    # 遍历第一个文件中的数据
    for item1 in data1:
        no1 = item1['No']
        answer1 = item1['answer']

        # 在第二个文件中查找相同的No
        for item2 in data2:
            no2 = item2['No']
            answer2 = item2['answer']
            question = item2['question']

            if no1 == no2:
                # 计算并保存结果
                if answer2 == "":
                    continue
                bleuscore = calculate_bleu(answer1, answer2)
                output_item = {
                    'No': no1,
                    'question': question,
                    'answer1': answer1,
                    'answer2': answer2,
                    'bluescore': bleuscore
                }
                total_score += bleuscore
                total += 1
                output_data.append(output_item)

    # 将结果保存到output.json文件中
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, ensure_ascii=False, indent=4)

    print(f"Output saved to {output_file}")
    print(f"Total records: {total}, Average score: {round(float(total_score) / total,9)}")

config = load_config("config.json")
model_name = config["model_name"]
model = model_name.split("/")[-1]

file1 = "../jsons/image_caption.json"
file2 = f"../output/{model}/image_caption_{model}.json"

save_dir = f"../output/{model}/eval_res"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print(f"Created {save_dir}")

output_file = f"{save_dir}/image_caption_{model}.json"
process_json_files(file1, file2, output_file)
