#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
加密工具类
提供常用的加密辅助函数
"""

import os
import base64
import hashlib
from typing import Union, Tuple

def generate_random_key(length: int = 32) -> bytes:
    """
    生成指定长度的随机密钥
    :param length: 密钥长度（字节）
    :return: 随机密钥
    """
    return os.urandom(length)

def generate_salt(length: int = 16) -> bytes:
    """
    生成随机盐值
    :param length: 盐值长度（字节）
    :return: 随机盐值
    """
    return os.urandom(length)

def hash_password(password: Union[str, bytes], salt: bytes = None) -> Tuple[bytes, bytes]:
    """
    使用PBKDF2算法对密码进行哈希
    :param password: 原始密码
    :param salt: 盐值（可选）
    :return: (哈希后的密码, 盐值)
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    if salt is None:
        salt = generate_salt()
    
    # 使用PBKDF2算法进行密码哈希
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password,
        salt,
        iterations=100000,
        dklen=32
    )
    
    return key, salt

def verify_password(password: Union[str, bytes], stored_hash: bytes, salt: bytes) -> bool:
    """
    验证密码
    :param password: 待验证的密码
    :param stored_hash: 存储的密码哈希
    :param salt: 存储的盐值
    :return: 验证结果
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # 计算输入密码的哈希值
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password,
        salt,
        iterations=100000,
        dklen=32
    )
    
    return key == stored_hash

def encode_base64(data: bytes) -> str:
    """
    将字节数据编码为Base64字符串
    :param data: 字节数据
    :return: Base64编码的字符串
    """
    return base64.b64encode(data).decode('utf-8')

def decode_base64(data: str) -> bytes:
    """
    将Base64字符串解码为字节数据
    :param data: Base64编码的字符串
    :return: 解码后的字节数据
    """
    return base64.b64decode(data.encode('utf-8'))

def calculate_file_hash(filename: str, algorithm: str = 'sha256', chunk_size: int = 8192) -> str:
    """
    计算文件的哈希值
    :param filename: 文件名
    :param algorithm: 哈希算法（sha256, sha512等）
    :param chunk_size: 读取块大小
    :return: 文件的哈希值（十六进制字符串）
    """
    hash_obj = hashlib.new(algorithm)
    
    with open(filename, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

def main():
    # 测试密码哈希
    password = "MySecretPassword123"
    print(f"原始密码: {password}")
    
    # 生成密码哈希
    hashed_password, salt = hash_password(password)
    print(f"哈希后的密码: {encode_base64(hashed_password)}")
    print(f"盐值: {encode_base64(salt)}")
    
    # 验证密码
    is_valid = verify_password(password, hashed_password, salt)
    print(f"密码验证结果: {'成功' if is_valid else '失败'}")
    
    # 测试错误密码
    wrong_password = "WrongPassword"
    is_valid = verify_password(wrong_password, hashed_password, salt)
    print(f"错误密码验证结果: {'成功' if is_valid else '失败'}")
    
    # 测试随机密钥生成
    key = generate_random_key(32)
    print(f"随机密钥: {encode_base64(key)}")
    
    # 测试文件哈希
    test_file = "test_file.txt"
    with open(test_file, "w") as f:
        f.write("This is a test file for hash calculation.")
    
    file_hash = calculate_file_hash(test_file)
    print(f"文件哈希值: {file_hash}")
    
    # 清理测试文件
    os.remove(test_file)

if __name__ == '__main__':
    main() 