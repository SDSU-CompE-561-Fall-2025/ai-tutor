from cryptography.fernet import Fernet, InvalidToken

from app.core.settings import settings

fernet = Fernet(settings.fernet_key.encode())


def encrypt_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()


def decrypt_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode()).decode()


def encrypt_message(message: str) -> str:
    """Encrypt a chat message."""
    return fernet.encrypt(message.encode()).decode()


def decrypt_message(encrypted_message: str) -> str:
    """Decrypt a chat message."""
    if not encrypted_message:
        return encrypted_message

    try:
        return fernet.decrypt(encrypted_message.encode()).decode()
    except (InvalidToken, Exception):  # noqa: BLE001
        # If decryption fails, return the message as-is (backward compatibility for unencrypted messages)
        return encrypted_message
