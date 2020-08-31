#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import json

"""
os_limit: None
对json相关的操作
"""


def to_json(data: dict):
    return json.dumps(data, ensure_ascii=False)


def to_json_file(data: dict, filename: str):
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False)


def parse_json(json_str: str):
    return json.loads(json_str)


def parse_json_file(filename: str):
    with open(filename, 'r', encoding='utf8') as file:
        return json.load(file)
