import json
import re
import numpy as np
import os
import sys
sys.path.append(os.path.abspath('../'))
from load_config import load_config


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def has_number(s):
    return bool(re.search(r'\d', s))


def calculate_mean_abs_error(answers, standard_answers):
    total_error = 0.0
    count = 0
    wrong = 0
    for answer, standard_answer in zip(answers, standard_answers):
        if answer['answer'] == "":
            continue
        response = answer['answer']
        if answer['No'] == standard_answer['No'] and has_number(response):
            ans = re.findall(r'-?\d*\.\d+|\-?\d+', response)[-1]
            stan = standard_answer['answer']
            total_error += abs((float(ans) - float(stan)))
            # print(f"No: {answer['No']}\t ans: {ans}\t stan: {stan}\t total_e: {total_error}")
            count += 1
        else:
            wrong += 1
            # print(f"ERROR! No: {answer['No']}, answer: {answer['answer']}")
    print(f"Wrong format answer numbers: {wrong}")
    res = total_error / count  if count > 0 else 0
    res = round(res, 2)
    return res

def calculate_acc(answers, standard_answers):
    correct = 0
    count = 0
    wrong = 0
    for answer, standard_answer in zip(answers, standard_answers):
        if answer['answer'] == "":
            continue
        response = answer['answer']
        if answer['No'] == standard_answer['No'] and has_number(response):
            ans = re.findall(r'-?\d*\.\d+|\-?\d+', response)[-1]
            stan = standard_answer['answer']
            ans = float(ans)
            if ans == stan:
                correct += 1
            # print(f"No: {answer['No']}\t ans: {ans}\t stan: {stan}\t correct: {correct}")
            count += 1
        else:
            wrong += 1
            # print(f"ERROR! No: {answer['No']}, answer: {answer['answer']}")
    print(f"Wrong format answer numbers: {wrong}")
    res = correct / count * 100 if count > 0 else 0
    res = round(res, 2)
    return res

def calculate_mean_squared_error(answers, standard_answers):
    total_error = 0.0
    count = 0
    wrong = 0
    for answer, standard_answer in zip(answers, standard_answers):
        if answer['No'] == standard_answer['No'] and has_number(answer['answer']):
            ans = re.findall(r'\d+', answer['answer'])[-1]
            stan = standard_answer['answer']
            total_error += abs((float(ans) - float(stan))) / float(stan)
            # print(f"No: {answer['No']}\t ans: {ans}\t stan: {stan}\t total_e: {total_error}")
            count += 1
        else:
            wrong += 1
            # print(f"No: {answer['No']}, answer: {answer['answer']}")
    print(f"Wrong format answer numbers: {wrong}")
    res = total_error / count * 100 if count > 0 else 0
    res = round(res, 2)
    return res


config = load_config("config.json")
model_name = config["model_name"]
model = model_name.split("/")[-1]
print(f"Model name: {model}")
print(f"Task name: count_average")
file1 = "../jsons/status.json"
file2 = f"../output/{model}/status_" + model + ".json"
# 加载JSON文件
answers = load_json(f'../output/{model}/count_average_{model}.json')
standard_answers = load_json('../jsons/count_average.json')
print("MAPE")
print(calculate_mean_squared_error(answers, standard_answers))
print("MAE")
print(calculate_mean_abs_error(answers, standard_answers))
print("ACC")
print(calculate_acc(answers, standard_answers))