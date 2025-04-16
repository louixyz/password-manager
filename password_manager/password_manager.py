'''
title: 密码本管理工具
filename: password_manager.py
version: 0.2
author: louixyz
timestamp: 2025-04-16
note: CLI 密码本，支持随机密码生成、唯一记录 hash、备注字段
'''

import json
import os
import hashlib
import random
import string
from datetime import datetime
from password_utils import generate_password, calculate_hash

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

PASSWORD_OPTIONS = {
    '1': ('纯数字 6 位', lambda: ''.join(random.choices(string.digits, k=6))),
    '2': ('纯数字 8 位', lambda: ''.join(random.choices(string.digits, k=8))),
    '3': ('数字 + 字母 + 特殊字符（8 位）',
          lambda: ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*()', k=8))),
    '4': ('数字 + 字母 + 特殊字符（12 位）',
          lambda: ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*()', k=12)))
}


def load_data():
    if not os.path.exists(DATA_FILE):
        # 自动初始化空文件
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_hash(entry):
    hash_input = ''.join(str(entry.get(field, '')) for field in [
        'id', 'username', 'email', 'phone', 'password', 'reg_date', 'timestamp', 'note'])
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()


def prompt_password():
    print("请选择密码生成规则：")
    for k, (desc, _) in PASSWORD_OPTIONS.items():
        print(f"{k}. {desc}")
    option = input("> ").strip()
    if option in PASSWORD_OPTIONS:
        return PASSWORD_OPTIONS[option][1]()
    else:
        print("⚠️ 无效选择，使用默认规则 3")
        return PASSWORD_OPTIONS['3'][1]()


def add_entry():
    data = load_data()
    new_id = str(len(data) + 1).zfill(3)

    username = input("用户名：").strip()
    email = input("邮箱：").strip()
    phone = input("电话：").strip()
    password = prompt_password()
    reg_date = input("注册日期 (留空使用今天)：").strip() or datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = input("备注：").strip()

    new_entry = {
        "id": new_id,
        "username": username,
        "email": email,
        "phone": phone,
        "password": password,
        "reg_date": reg_date,
        "timestamp": timestamp,
        "note": note
    }
    new_entry["hash"] = generate_hash(new_entry)
    data.append(new_entry)
    save_data(data)
    print("✅ 添加成功！")


def list_entries():
    data = load_data()
    if not data:
        print("📭 没有记录。")
        return
    for item in data:
        print("-" * 40)
        for k, v in item.items():
            print(f"{k}: {v}")
    print("-" * 40)


def main():
    while True:
        print("\n📘 密码本管理工具")
        print("1. 添加记录")
        print("2. 查看所有记录")
        print("3. 退出")
        choice = input("> ").strip()

        if choice == '1':
            add_entry()
        elif choice == '2':
            list_entries()
        elif choice == '3':
            print("👋 再见！")
            break
        else:
            print("⚠️ 无效输入")


if __name__ == '__main__':
    main()