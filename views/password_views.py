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
        value = cls._get_random_string()
        #Essa linha pega a string aleatória (value), a codifica para o formato utf-8 com value.encode('utf-8'), e então aplica o algoritmo de hash SHA-256 (usado para gerar um valor de hash único e de comprimento fixo) usando hashlib.sha256().

        #.digest() retorna o hash resultante como uma sequência de bytes.
        hasher = hashlib.sha256(value.encode('utf-8')).digest()

        #Aqui, o hash gerado (hasher) é codificado para o formato Base64 usando base64.b64encode(). O Base64 é uma forma de representar dados binários (como um hash) em uma string ASCII, tornando-o legível e mais fácil de armazenar.
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

        return cls.KEY_DIR / arq
    
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