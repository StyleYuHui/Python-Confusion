#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RSA公钥密码示例
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

class RSAEncryption:
    def __init__(self, key_size=2048):
        """
        初始化RSA加密器
        :param key_size: 密钥大小（位）
        """
        self.key_size = key_size
        self.key = RSA.generate(key_size)
        self.public_key = self.key.publickey()
    
    def save_keys(self, private_file: str, public_file: str) -> None:
        """
        保存密钥对
        :param private_file: 私钥文件名
        :param public_file: 公钥文件名
        """
        # 保存私钥
        with open(private_file, 'wb') as f:
            f.write(self.key.export_key('PEM'))
        
        # 保存公钥
        with open(public_file, 'wb') as f:
            f.write(self.public_key.export_key('PEM'))
    
    def load_private_key(self, filename: str) -> None:
        """
        加载私钥
        :param filename: 私钥文件名
        """
        with open(filename, 'rb') as f:
            self.key = RSA.import_key(f.read())
            self.public_key = self.key.publickey()
    
    def load_public_key(self, filename: str) -> None:
        """
        加载公钥
        :param filename: 公钥文件名
        """
        with open(filename, 'rb') as f:
            self.public_key = RSA.import_key(f.read())
    
    def encrypt(self, data: bytes) -> bytes:
        """
        使用公钥加密数据
        :param data: 要加密的数据
        :return: 加密后的数据
        """
        cipher = PKCS1_OAEP.new(self.public_key)
        return cipher.encrypt(data)
    
    def decrypt(self, data: bytes) -> bytes:
        """
        使用私钥解密数据
        :param data: 要解密的数据
        :return: 解密后的数据
        """
        cipher = PKCS1_OAEP.new(self.key)
        return cipher.decrypt(data)
    
    def sign(self, data: bytes) -> bytes:
        """
        使用私钥签名数据
        :param data: 要签名的数据
        :return: 签名
        """
        hash_obj = SHA256.new(data)
        signature = pkcs1_15.new(self.key).sign(hash_obj)
        return signature
    
    def verify(self, data: bytes, signature: bytes) -> bool:
        """
        使用公钥验证签名
        :param data: 原始数据
        :param signature: 签名
        :return: 验证结果
        """
        hash_obj = SHA256.new(data)
        try:
            pkcs1_15.new(self.public_key).verify(hash_obj, signature)
            return True
        except (ValueError, TypeError):
            return False

def main():
    # 创建RSA实例
    rsa = RSAEncryption()
    
    # 测试数据
    message = b"This is a test message for RSA encryption and signing."
    
    # 加密/解密示例
    print("=== 加密/解密示例 ===")
    print(f"原始消息: {message}")
    
    # 加密
    ciphertext = rsa.encrypt(message)
    print(f"加密后: {base64.b64encode(ciphertext).decode()}")
    
    # 解密
    decrypted = rsa.decrypt(ciphertext)
    print(f"解密后: {decrypted}")
    print(f"验证结果: {'成功' if decrypted == message else '失败'}")
    
    # 签名/验证示例
    print("\n=== 签名/验证示例 ===")
    print(f"消息: {message}")
    
    # 签名
    signature = rsa.sign(message)
    print(f"签名: {base64.b64encode(signature).decode()}")
    
    # 验证
    is_valid = rsa.verify(message, signature)
    print(f"验证结果: {'成功' if is_valid else '失败'}")
    
    # 保存和加载密钥示例
    print("\n=== 密钥管理示例 ===")
    rsa.save_keys('private.pem', 'public.pem')
    print("密钥已保存到 private.pem 和 public.pem")
    
    # 创建新的RSA实例并加载密钥
    new_rsa = RSAEncryption()
    new_rsa.load_private_key('private.pem')
    
    # 使用加载的密钥测试
    ciphertext = new_rsa.encrypt(message)
    decrypted = new_rsa.decrypt(ciphertext)
    print(f"使用加载的密钥验证结果: {'成功' if decrypted == message else '失败'}")

if __name__ == '__main__':
    main() 