'''
title: 密码工具模块
filename: password_utils.py
version: 0.1
author: louixyz
timestamp: 2025-04-16
note: 提供密码生成与哈希计算功能
'''

import random
import string
import hashlib


def generate_password(option: int) -> str:
    """
    根据选项生成不同复杂度的密码
    option:
        1 - 6位纯数字
        2 - 8位纯数字
        3 - 8位数字+字母+特殊字符
        4 - 12位数字+字母+特殊字符
    """
    if option == 1:
        chars = string.digits
        length = 6
    elif option == 2:
        chars = string.digits
        length = 8
    elif option == 3:
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        length = 8
    elif option == 4:
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        length = 12
    else:
        raise ValueError("密码生成选项无效")

    return ''.join(random.choice(chars) for _ in range(length))


def calculate_hash(record: dict) -> str:
    """
    根据用户记录生成唯一 hash 值，用于标识和搜索
    """
    fields = ['id', 'username', 'email', 'phone', 'password', 'reg_date', 'timestamp', 'note']
    raw_string = ''.join(str(record.get(field, '')) for field in fields)
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()