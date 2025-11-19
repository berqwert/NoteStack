"""Simple encryption utilities for note storage"""
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
from config import DATA_DIR

KEY_FILE = os.path.join(DATA_DIR, ".key")


def get_or_create_key(password: str = None) -> bytes:
    """
    Get encryption key from file or create new one
    
    Args:
        password: Optional password to derive key from. If None, uses stored key.
    
    Returns:
        Encryption key as bytes
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if password:
        # Derive key from password
        salt = b'notestack_salt_2025'  # Fixed salt for simplicity
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key


def encrypt_data(data: str, key: bytes = None) -> bytes:
    """
    Encrypt string data
    
    Args:
        data: String to encrypt
        key: Encryption key (uses default if None)
    
    Returns:
        Encrypted bytes
    """
    if key is None:
        key = get_or_create_key()
    
    fernet = Fernet(key)
    return fernet.encrypt(data.encode('utf-8'))


def decrypt_data(encrypted_data: bytes, key: bytes = None) -> str:
    """
    Decrypt bytes to string
    
    Args:
        encrypted_data: Encrypted bytes
        key: Encryption key (uses default if None)
    
    Returns:
        Decrypted string
    """
    if key is None:
        key = get_or_create_key()
    
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode('utf-8')

