import json
import re
import os
import sys
from collections import Counter

sys.path.append(os.path.abspath('../'))
from load_config import load_config


def normalize_answer(answer):
    # 去除多余的空格，并统一分隔符
    answer = answer.replace('\n', '')
    answer = answer.replace(' ', '')
    answer = answer.replace("；", ";")
    answer = answer.replace("：", ": ")
    answer = answer.replace("图案", "")
    answer = answer.replace("散点式", "")
    answer = answer.replace("。", "")
    answer = answer.replace("/", "、")
    answer = answer.replace("地毯、窗帘", "地毯")
    answer = answer.replace("窗帘", "地毯")
    answer = answer.replace("地毯、地毯", "地毯")
    answer = answer.replace("地毯或地毯", "地毯")
    answer = answer.replace("地毯地毯", "地毯")
    answer = answer.replace("平棋、人字披", "平棋")
    answer = answer.replace("人字披", "平棋")
    answer = answer.replace("平棋平棋", "平棋")
    answer = answer.replace("1: ", "")
    answer = answer.replace("2: ", "")
    answer = answer.replace("3: ", "")
    answer = answer.replace("4: ", "")
    answer = answer.replace("1: ", "")
    answer = answer.replace("2: ", "")
    answer = answer.replace("3: ", "")
    answer = answer.replace("第一张: ", "")
    answer = answer.replace("第二张: ", "")
    answer = answer.replace("第三张: ", "")
    answer = answer.replace("第四张: ", "")
    answer = answer.strip()
    return answer


def find_unique_index(lst):
    counts = Counter(lst)  # 统计每个元素出现的次数
    unique_count = sum(1 for count in counts.values() if count == 1)  # 计算出现次数为1的元素个数
    if unique_count > 1:
        return -1  # 如果有多个count为1的元素，返回-1

    for index, value in enumerate(lst):
        if counts[value] == 1:
            return index  # 找到唯一不同元素的下标

    return -1  # 如果没有count为1的元素，返回-1


def compare_json_answers(file1, file2):
    try:
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
        matches = []
        mismatches = []
        total_records = 0
        correct_matches = 0

        for record1, record2 in zip(data1, data2):
            if record1['No'] != record2['No']:
                print(f"Mismatch in No fields: {record1['No']} != {record2['No']}")
                continue

            total_records += 1

            # 标准化 answer 字段
            normalized_answer1 = normalize_answer(record1['answer'])
            list1 = [item.strip() for item in normalized_answer1.split(';') if item.strip()]
            normalized_answer2 = normalize_answer(record2['answer'])
            list2 = [item.strip() for item in normalized_answer2.split(';') if item.strip()]
            index1 = find_unique_index(list1)
            index2 = find_unique_index(list2)
            if normalized_answer1 in normalized_answer2:
                matches.append({
                    'No': record1['No'],
                    'file1_answer': normalized_answer1,
                    'file2_answer': normalized_answer2
                })
                correct_matches += 1
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
        for match in matches:
            print(
                f"No: {match['No']}, File1 Answer: {match['file1_answer']}, File2 Answer: {match['file2_answer']}")
        if mismatches:
            print("Mismatched answers:")
            for mismatch in mismatches:
                print(
                    f"No: {mismatch['No']}, File1 Answer: {mismatch['file1_answer']}, File2 Answer: {mismatch['file2_answer']}")
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
print(f"Task name: image-classification")
file1 = "../jsons/image_classification.json"
file2 = f"../output/{model}/image_classification_" + model + ".json"
compare_json_answers(file1, file2)
