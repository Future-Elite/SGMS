import os
import hashlib


def generate_salt(length=16):
    """
    生成随机盐，返回hex字符串，默认16字节（32字符）
    """
    return os.urandom(length).hex()


def hash_password(password: str, salt: str) -> str:
    """
    使用sha256对 salt + password 进行哈希，返回64字符十六进制字符串
    """
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()


def verify_password(stored_hash: str, salt: str, provided_password: str) -> bool:
    """
    验证密码是否匹配
    """
    return stored_hash == hash_password(provided_password, salt)
