#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AES分组密码示例
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESEncryption:
    def __init__(self, key_size=256):
        """
        初始化AES加密器
        :param key_size: 密钥大小（128/192/256位）
        """
        self.key_size = key_size
        self.key = get_random_bytes(key_size // 8)
        self.iv = get_random_bytes(16)  # 初始化向量
    
    def encrypt(self, data):
        """
        加密数据
        :param data: 要加密的数据（字节串）
        :return: (加密后的数据, 初始化向量)
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext, self.iv
    
    def decrypt(self, ciphertext, iv):
        """
        解密数据
        :param ciphertext: 加密后的数据（字节串）
        :param iv: 初始化向量
        :return: 解密后的数据（字节串）
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(ciphertext)
        return unpad(padded_data, AES.block_size)
    
    def save_key(self, filename):
        """
        保存密钥
        :param filename: 文件名
        """
        with open(filename, 'wb') as f:
            f.write(self.key)
    
    def load_key(self, filename):
        """
        加载密钥
        :param filename: 文件名
        """
        with open(filename, 'rb') as f:
            self.key = f.read()

def main():
    # 创建AES加密器实例
    aes = AESEncryption()
    
    # 测试数据
    plaintext = b'This is a test message for AES encryption. It needs to be long enough to demonstrate padding.'
    
    # 加密
    ciphertext, iv = aes.encrypt(plaintext)
    print(f"原始数据: {plaintext}")
    print(f"加密后: {ciphertext}")
    
    # 解密
    decrypted = aes.decrypt(ciphertext, iv)
    print(f"解密后: {decrypted}")
    
    # 验证
    print(f"验证结果: {'成功' if decrypted == plaintext else '失败'}")
    
    # 保存和加载密钥示例
    aes.save_key('aes_key.bin')
    new_aes = AESEncryption()
    new_aes.load_key('aes_key.bin')
    
    # 使用加载的密钥测试
    ciphertext, iv = new_aes.encrypt(plaintext)
    decrypted = new_aes.decrypt(ciphertext, iv)
    print(f"使用加载的密钥验证结果: {'成功' if decrypted == plaintext else '失败'}")

if __name__ == '__main__':
    main() 