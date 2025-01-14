import urllib.parse
from common import SingletonMeta
from fastapi import Query
from typing import Annotated, Literal
from services.vnpay.models import VNPayKey, VNPayProduct, VNPaySandBox
from services.vnpay.models.response import PaymentResponse


class Base:
    version = '2.1.0'
    url_sandbox = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    url_product = ""
    def __init__(self, *,
                 env : Annotated[Literal["sandbox", "product"], Query(description = "Select environment")],
                 from_init: bool = False, **kwargs
                 ) -> None:
        self.env: str = env
        self.sandbox : VNPayKey = None
        self.product : VNPayKey = None
        if from_init:
            self.__from_init(**kwargs)
        else:
            self.__from_instance(**kwargs)
            

                                    
    def __from_init(self, **kwargs) -> None:
        terminal_code_sandbox = kwargs.get('terminal_code_sandbox')
        secret_key_sandbox = kwargs.get('secret_key_sandbox')
        terminal_code_production = kwargs.get('terminal_code_production')
        secret_key_production = kwargs.get('secret_key_production')
        self.sandbox = VNPaySandBox(terminal_code=terminal_code_sandbox, 
                                    secret_key=secret_key_sandbox).create_hash()
        self.product = VNPayProduct(terminal_code=terminal_code_production, 
                                    secret_key=secret_key_production).create_hash()
    
    def __from_instance(self, **kwargs) -> None:
        self.sandbox : VNPaySandBox = kwargs.get('sandbox').create_hash()
        self.product : VNPayProduct = kwargs.get('product').create_hash()
        
    def verify(self, data_response : PaymentResponse) -> bool:
        data_dict = data_response.dict()
        vnp_SecureHash = data_dict.pop('vnp_SecureHash')
        data_str = urllib.parse.urlencode(data_dict)
        hash_value = self.hash.hmac_sha256(data = data_str)
        return hash_value == vnp_SecureHash