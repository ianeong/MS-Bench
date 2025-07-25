import json
import re
import os
import sys
sys.path.append(os.path.abspath('../'))
from load_config import load_config


def normalize_answer(answer):
    answer = answer.replace("。", "")
    answer = answer.strip()
    return answer

def compare_json_answers(file1, file2):
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        mismatches = []
        matches = []
        total_records = 0
        correct_matches = 0

        for record1, record2 in zip(data1, data2):
            if record1['No'] != record2['No']:
                print(f"Mismatch in No fields: {record1['No']} != {record2['No']}")
                continue

            total_records += 1

            # 标准化 answer 字段
            normalized_answer1 = normalize_answer(record1['answer'])
            normalized_answer2 = normalize_answer(record2['answer'])

            if normalized_answer1 in normalized_answer2:
                correct_matches += 1
                matches.append({
                    'No': record1['No'],
                    'file1_answer': normalized_answer1,
                    'file2_answer': normalized_answer2
                })

            else:
                mismatches.append({
                    'No': record1['No'],
                    'file1_answer': normalized_answer1,
                    'file2_answer': normalized_answer2
                })

        accuracy = (correct_matches / total_records) * 100 if total_records > 0 else 0

        print(f"Total records compared: {total_records}")
        print(f"Correct matches: {correct_matches}")
        print(f"Accuracy: {accuracy:.2f}%")

        if mismatches:
            print(f"Matched answers:")
            for match in matches:
                print(f"No: {match['No']}, File1 Answer: {match['file1_answer']}, File2 Answer: {match['file2_answer']}")
            print("Mismatched answers:")
            for mismatch in mismatches:
                print(f"No: {mismatch['No']}, File1 Answer: {mismatch['file1_answer']}, File2 Answer: {mismatch['file2_answer']}")
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
print(f"Task name: variant_most")
file1 = "../jsons/variant_most.json"
file2 = f"../output/{model}/variant_most_"+model+".json"
compare_json_answers(file1, file2)
