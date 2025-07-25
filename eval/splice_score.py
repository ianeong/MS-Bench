import json
import re
import os
import sys
sys.path.append(os.path.abspath('../'))
from load_config import load_config


def normalize_answer(answer):
    answer = re.findall(r'\d+', answer)
    # 没有评分，输出-1
    if len(answer) == 0:
        return -1
    # 默认第一个数字是分数
    answer = answer[0]
    return answer

def compare_json_answers(file1, file2):
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        mismatches = []
        total_records = 0
        score_sum = 0
        for record1, record2 in zip(data1, data2):
            if record1['No'] != record2['No']:
                print(f"Mismatch in No fields: {record1['No']} != {record2['No']}")
                continue

            total_records += 1
            score1 = int(normalize_answer(record1['answer']))
            score2 = int(normalize_answer(record2['answer']))
            final_score = 0
            if score2 == -1:
                final_score = 0
            else:
                if score2 >= 70:
                    score2 = 100
                else:
                    score2 = 0
                final_score = 100-abs(score1 - score2)

            if score1 != score2:
                mismatches.append({
                    'No': record1['No'],
                    'file1_score': score1,
                    'file2_score': score2
                })
            score_sum += final_score

        accuracy = score_sum / total_records

        print(f"Total records compared: {total_records}")
        print(f"Accuracy: {accuracy:.2f}%")

        if mismatches:
            print("Mismatched answers:")
            for mismatch in mismatches:
                print(f"No: {mismatch['No']}, File1 Answer: {mismatch['file1_score']}, File2 Answer: {mismatch['file2_score']}")
        else:
            print("All answers match.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
    except KeyError as e:
        print(f"Missing expected key in data: {e}")

config = load_config("config.json")
model_name = config["model_name"]
model = model_name.split("/")[-1]
print(f"Model name: {model}")
print(f"Task name: splice_score")
file1 = "../jsons/splice_score.json"
file2 = f"../output/{model}/splice_score_"+model+".json"
compare_json_answers(file1, file2)
