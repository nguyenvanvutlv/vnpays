from pydantic import BaseModel
from typing import TypeVar, Optional, Generic
from fastapi import status

T = TypeVar('T')


class ResponseModel(BaseModel):
    __abstract__ = True

    status_code: int = status.HTTP_200_OK
    message_response: str = 'OK'

    def response(
        self,
        status_code: int = status.HTTP_200_OK,
        message_response: str = 'OK'
    ) -> "ResponseModel":
        self.status_code = status_code
        self.message_response = message_response
        return self
    
class PayLoadModel(ResponseModel, BaseModel, Generic[T]):

    data : Optional[T] = None
    class Config:
        arbitrary_types_allowed = True

    def response(
        self,
        status_code: int = status.HTTP_200_OK,
        message_response: str = 'OK',
        data: T = None
    ) -> "PayLoadModel":
        self.status_code = status_code
        self.message_response = message_response
        self.data = data
        return self
    

class BaseSchemas(BaseModel):
    __abstract__ = True

    def dict(self):
        return self.model_dump()