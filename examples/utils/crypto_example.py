#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
加密工具使用示例
展示如何使用加密工具类进行各种加密操作
"""

from crypto_utils import (
    generate_random_key,
    hash_password,
    verify_password,
    encode_base64,
    decode_base64,
    calculate_file_hash
)
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    """
    使用AES加密数据
    :param data: 要加密的数据
    :param key: 密钥
    :return: 加密后的数据
    """
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes

def aes_decrypt(data: bytes, key: bytes) -> bytes:
    """
    使用AES解密数据
    :param data: 要解密的数据
    :param key: 密钥
    :return: 解密后的数据
    """
    iv = data[:16]
    ct = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)

def main():
    print("=== 加密工具使用示例 ===\n")
    
    # 1. 密码哈希示例
    print("1. 密码哈希示例")
    password = "MySecretPassword123"
    hashed_password, salt = hash_password(password)
    print(f"原始密码: {password}")
    print(f"哈希后的密码: {encode_base64(hashed_password)}")
    print(f"盐值: {encode_base64(salt)}")
    print(f"验证结果: {'成功' if verify_password(password, hashed_password, salt) else '失败'}\n")
    
    # 2. AES加密示例
    print("2. AES加密示例")
    message = b"This is a secret message that needs to be encrypted."
    key = generate_random_key(32)  # AES-256需要32字节密钥
    
    # 加密
    encrypted = aes_encrypt(message, key)
    print(f"原始消息: {message}")
    print(f"加密后: {encode_base64(encrypted)}")
    
    # 解密
    decrypted = aes_decrypt(encrypted, key)
    print(f"解密后: {decrypted}")
    print(f"验证结果: {'成功' if decrypted == message else '失败'}\n")
    
    # 3. 文件哈希示例
    print("3. 文件哈希示例")
    test_file = "test_file.txt"
    test_content = "This is a test file for hash calculation."
    
    # 创建测试文件
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 计算文件哈希
    file_hash = calculate_file_hash(test_file)
    print(f"文件内容: {test_content}")
    print(f"文件哈希值: {file_hash}")
    
    # 清理测试文件
    os.remove(test_file)
    print("\n测试文件已清理")

if __name__ == '__main__':
    main() 