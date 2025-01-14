from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Query
from services.vnpay.hash import Hashing

class VNPayKey(BaseModel):
    terminal_code: Annotated[str, Query(description="Terminal code VNPAY")]
    secret_key: Annotated[str, Query(description="Secret key VNPAY")]
    _hash : Annotated[Hashing, Query(description="Create hash for VNPAY")] = None
    
    
    def dict(self) -> dict:
        return self.model_dump()
    
    def create_hash(self) -> "VNPayKey":
        if self._hash is None:
            self._hash = Hashing(secret_key = self.secret_key)
        return self
    
    def hash_data(self, data: str) -> str:
        return self._hash.hmac_sha256(data = data)
    
class VNPaySandBox(VNPayKey):
    pass


class VNPayProduct(VNPayKey):
    pass
