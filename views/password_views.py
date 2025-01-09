import string, secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / "keys"

    def __init__(self, key):
        #se chave nao for uma instancia de bytes
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)


    @classmethod
    def _get_random_string(cls, length=25):
        string = ''
        for i in range(length):
            string += secrets.choice(cls.RANDOM_STRING_CHARS)
        return string
    
    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_string
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        else:
            return key, None
        

    @classmethod
    def archive_key(cls, key):
        arq = "key.key"
        if Path(cls.KEY_DIR / arq).exists():
            arq = f"key_{cls._get_random_string(length=5)}.key"

        with open(cls.KEY_DIR / arq, "wb") as file:
            file.write(key)

        return cls.KEY_DIR / file
    
    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)
    
    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e:
            return f"Token Inválida | Detalhes do erro: {e}"