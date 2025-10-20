from cryptography.fernet import Fernet

from app.core.settings import settings

fernet = Fernet(settings.feret_key)


def encrypt_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()


def decrypt_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode()).decode()
