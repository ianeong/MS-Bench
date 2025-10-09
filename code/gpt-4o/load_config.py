import json


def load_config(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config
