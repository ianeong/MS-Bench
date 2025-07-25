import json
import re
import numpy as np

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
        response = answer['answer'].split('\n')[-1]

        if answer['No'] == standard_answer['No'] and has_number(response):
            ans = re.findall(r'-?\d*\.\d+|\-?\d+', response)[-1]
            stan = standard_answer['answer']
            total_error += abs((float(ans) - float(stan))) 
            print(f"No: {answer['No']}\t ans: {ans}\t stan: {stan}\t total_e: {total_error}")
            count += 1
        else:
            wrong += 1
            print(f"ERROR! No: {answer['No']}, answer: {answer['answer']}")
    print(f"Wrong format answer numbers: {wrong}")
    return total_error / count  if count > 0 else 0

def calculate_acc(answers, standard_answers):
    correct = 0
    count = 0
    wrong = 0
    for answer, standard_answer in zip(answers, standard_answers):
        if answer['answer'] == "":
            continue    
        response = answer['answer'].split('\n')[-1]

        if answer['No'] == standard_answer['No'] and has_number(response):
            ans = re.findall(r'-?\d*\.\d+|\-?\d+', response)[-1]
            stan = standard_answer['answer']
            if int(ans) == stan:
                correct += 1
            print(f"No: {answer['No']}\t ans: {ans}\t stan: {stan}\t correct: {correct}")
            count += 1
        else:
            wrong += 1
            print(f"ERROR! No: {answer['No']}, answer: {answer['answer']}")
    print(f"Wrong format answer numbers: {wrong}")
    return correct / count * 100 if count > 0 else 0



# 加载JSON文件
answers = load_json('/count_average_qwen.json')
standard_answers = load_json('json/count_average.json')

print(f"{calculate_mean_abs_error(answers, standard_answers)}")
print(f"{calculate_acc(answers, standard_answers)}%")