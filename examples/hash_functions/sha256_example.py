#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SHA-256哈希函数示例
"""

import hashlib
import hmac
import os
from typing import Union, Tuple

class SHA256Hash:
    def __init__(self):
        """初始化SHA-256哈希器"""
        self.hash_obj = hashlib.sha256()
    
    def update(self, data: Union[str, bytes]) -> None:
        """
        更新哈希值
        :param data: 要哈希的数据（字符串或字节串）
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.hash_obj.update(data)
    
    def digest(self) -> bytes:
        """
        获取哈希值（字节串）
        :return: 哈希值
        """
        return self.hash_obj.digest()
    
    def hexdigest(self) -> str:
        """
        获取哈希值（十六进制字符串）
        :return: 哈希值
        """
        return self.hash_obj.hexdigest()
    
    def reset(self) -> None:
        """重置哈希器"""
        self.hash_obj = hashlib.sha256()

class HMAC_SHA256:
    def __init__(self, key: Union[str, bytes] = None):
        """
        初始化HMAC-SHA256
        :param key: 密钥（字符串或字节串）
        """
        if key is None:
            key = os.urandom(32)  # 生成随机密钥
        if isinstance(key, str):
            key = key.encode('utf-8')
        self.key = key
    
    def sign(self, message: Union[str, bytes]) -> bytes:
        """
        签名消息
        :param message: 要签名的消息（字符串或字节串）
        :return: 签名（字节串）
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.new(self.key, message, hashlib.sha256).digest()
    
    def verify(self, message: Union[str, bytes], signature: bytes) -> bool:
        """
        验证签名
        :param message: 消息（字符串或字节串）
        :param signature: 签名（字节串）
        :return: 验证结果
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        return hmac.compare_digest(self.sign(message), signature)

def hash_file(filename: str) -> Tuple[str, str]:
    """
    计算文件的SHA-256哈希值
    :param filename: 文件名
    :return: (文件哈希值, 文件大小)
    """
    sha256 = hashlib.sha256()
    size = 0
    
    with open(filename, 'rb') as f:
        while True:
            data = f.read(65536)  # 每次读取64KB
            if not data:
                break
            sha256.update(data)
            size += len(data)
    
    return sha256.hexdigest(), str(size)

def main():
    # 基本哈希示例
    print("=== 基本哈希示例 ===")
    sha256 = SHA256Hash()
    message = "Hello, this is a test message for SHA-256 hashing!"
    sha256.update(message)
    print(f"消息: {message}")
    print(f"SHA-256哈希值: {sha256.hexdigest()}")
    
    # HMAC示例
    print("\n=== HMAC示例 ===")
    hmac_sha256 = HMAC_SHA256("SecretKey123")
    message = "This is a test message for HMAC-SHA256"
    signature = hmac_sha256.sign(message)
    print(f"消息: {message}")
    print(f"HMAC-SHA256签名: {signature.hex()}")
    print(f"验证结果: {hmac_sha256.verify(message, signature)}")
    
    # 文件哈希示例
    print("\n=== 文件哈希示例 ===")
    # 创建测试文件
    test_file = "test_file.txt"
    with open(test_file, "w") as f:
        f.write("This is a test file for SHA-256 hashing.\n")
        f.write("It contains multiple lines of text.\n")
    
    file_hash, file_size = hash_file(test_file)
    print(f"文件名: {test_file}")
    print(f"文件大小: {file_size} 字节")
    print(f"文件SHA-256哈希值: {file_hash}")
    
    # 清理测试文件
    os.remove(test_file)

if __name__ == '__main__':
    main() 