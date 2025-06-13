#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RC4流密码示例
"""

class RC4:
    def __init__(self, key):
        """
        初始化RC4密码器
        :param key: 密钥（字节串）
        """
        self.key = key
        self.S = list(range(256))
        self._init_state()
    
    def _init_state(self):
        """初始化状态向量"""
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
    
    def _generate_keystream(self, length):
        """生成密钥流"""
        i = j = 0
        keystream = []
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            k = self.S[(self.S[i] + self.S[j]) % 256]
            keystream.append(k)
        return keystream
    
    def encrypt(self, data):
        """
        加密数据
        :param data: 要加密的数据（字节串）
        :return: 加密后的数据（字节串）
        """
        keystream = self._generate_keystream(len(data))
        return bytes(a ^ b for a, b in zip(data, keystream))
    
    def decrypt(self, data):
        """
        解密数据
        :param data: 要解密的数据（字节串）
        :return: 解密后的数据（字节串）
        """
        return self.encrypt(data)  # RC4是对称的，加密和解密使用相同的操作

def main():
    # 测试密钥和数据
    key = b'SecretKey123'
    plaintext = b'Hello, this is a test message for RC4 encryption!'
    
    # 创建RC4实例
    rc4 = RC4(key)
    
    # 加密
    ciphertext = rc4.encrypt(plaintext)
    print(f"原始数据: {plaintext}")
    print(f"加密后: {ciphertext}")
    
    # 解密
    decrypted = rc4.decrypt(ciphertext)
    print(f"解密后: {decrypted}")
    
    # 验证
    print(f"验证结果: {'成功' if decrypted == plaintext else '失败'}")

if __name__ == '__main__':
    main() 