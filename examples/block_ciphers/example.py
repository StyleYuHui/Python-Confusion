import struct

DELTA = 0x9e3779b9  # 常量 delta
NUM_ROUNDS = 32  # TEA 默认轮数


def encrypt(v, k):
    v0, v1 = v
    k0, k1, k2, k3 = k
    sum = 0
    for _ in range(NUM_ROUNDS):
        sum = (sum + DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    return v0, v1


def decrypt(v, k):
    v0, v1 = v
    k0, k1, k2, k3 = k
    sum = (DELTA * NUM_ROUNDS) & 0xFFFFFFFF
    for _ in range(NUM_ROUNDS):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        sum = (sum - DELTA) & 0xFFFFFFFF
    return v0, v1


def str_to_uint32_list(s):
    s = s.encode('utf-8')
    while len(s) % 8 != 0:
        s += b'\0'
    return [struct.unpack('>2I', s[i:i + 8]) for i in range(0, len(s), 8)]


def uint32_list_to_str(lst):
    s = b''.join([struct.pack('>2I', *v) for v in lst])
    return s.rstrip(b'\0').decode('utf-8')


def main():
    key = (0x01234567, 0x89abcdef, 0xfedcba98, 0x76543210)  # 128位密钥
    plaintext = "Hello TEA Encryption!"

    # 加密
    data = str_to_uint32_list(plaintext)
    encrypted_data = [encrypt(block, key) for block in data]
    print("Encrypted:", encrypted_data)

    # 解密
    decrypted_data = [decrypt(block, key) for block in encrypted_data]
    decrypted_text = uint32_list_to_str(decrypted_data)
    print("Decrypted:", decrypted_text)


if __name__ == '__main__':
    main()
