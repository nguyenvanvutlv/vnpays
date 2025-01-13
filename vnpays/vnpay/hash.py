import hashlib
import hmac
from vnpay import SingletonMeta


class Hashing(metaclass = SingletonMeta):
    
    def __init__(self, secret_key: str) -> None:
        self.__secret_key = secret_key.encode('utf-8')
        
    def change_key(self, secret_key: str) -> None:
        self.__secret_key = secret_key.encode('utf-8')
    
    def hmac_sha256(self, *, data: str) -> str:
        byteData = data.encode('utf-8')
        return hmac.new(self.__secret_key, byteData, hashlib.sha512).hexdigest()