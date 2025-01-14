from typing import TypeVar, Type, Annotated, Literal
from fastapi import Query
from services.vnpay.cmd import Base
from services.vnpay.cmd import OrderWooCommer
from config.configs import get_config
from common import SingletonMeta


T = TypeVar('T', bound = Base)


class VNPAYs(Base, metaclass = SingletonMeta):
    
    def _get_instance(self, cls: Type[T], *args, **kwargs) -> T:
        return cls(*args, from_init = False, sandbox = self.sandbox, product = self.product, **kwargs)


    def payment(self, env: str) -> OrderWooCommer:
        return self._get_instance(OrderWooCommer, env = env)


    def refund(self) -> None:
        pass


def getVNPayService() -> VNPAYs:
    __config = get_config()
    env = __config.get_config('ENV')
    terminal_code_sandbox = __config.get_config('TERMINAL_CODE_SANDBOX')
    secret_key_sandbox = __config.get_config('SECRET_KEY_SANDBOX')
    terminal_code_production = __config.get_config('TERMINAL_CODE_PRODUCTION')
    secret_key_production = __config.get_config('SECRET_KEY_PRODUCTION')
    return VNPAYs(env = env,
                    from_init = True,
                    terminal_code_sandbox = terminal_code_sandbox,
                    secret_key_sandbox = secret_key_sandbox,
                    terminal_code_production = terminal_code_production,
                    secret_key_production = secret_key_production)


# from common import SingletonMeta
# from datetime import datetime, timedelta
# from services.vnpay.models.requests import PaymentModel
# from services.vnpay.models.response import PaymentResponse
# from services.vnpay.hash import Hashing
# import urllib.parse


# class VNPAY(metaclass = SingletonMeta):
#     def __init__(self, 
#                  base_url: str, 
#                  return_url: str,
#                  version: str, 
#                  terminal_code: str,
#                  secret_key: str
#                  ) -> None:
#         self.base_url = base_url
#         self.return_url = return_url
#         self.version = version
#         self.terminal_code = terminal_code
#         self.hash = Hashing(secret_key = secret_key)
        
        
#     def change_url(self, base_url: str, version: str, terminal_code: str) -> None:
#         self.base_url = base_url
#         self.version = version
#         self.terminal_code = terminal_code
        
#     def validate_payment(self, data: PaymentResponse) -> bool:
#         data_dict = data.dict()
#         vnp_SecureHash = data_dict.pop('vnp_SecureHash')
#         data_str = urllib.parse.urlencode(data_dict)
#         hash_value = self.hash.hmac_sha256(data = data_str)
#         return hash_value == vnp_SecureHash
        
        
#     def create_payment(self, order_id: str, 
#                        vnp_Amount: int, 
#                        vnp_IpAddr: str,
#                        vnp_OrderInfo : str,
#                        limit_time: int = 15,
#                        vnp_OrderType : str = 'billpayment',
#                        vnp_Locale : str = 'vn',
#                        vnp_CurrCode: str = "VND",
#                        ) -> str:
#         vnp_OrderInfo = urllib.parse.quote_plus(vnp_OrderInfo)
#         payment_model = PaymentModel(
#             vnp_Version = self.version,
#             vnp_Command = 'pay',
#             vnp_TmnCode = self.terminal_code,
#             vnp_Amount = vnp_Amount,
#             vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S'),
#             vnp_CurrCode = vnp_CurrCode,
#             vnp_IpAddr = vnp_IpAddr,
#             vnp_Locale = vnp_Locale,
#             vnp_OrderInfo = vnp_OrderInfo,
#             vnp_OrderType = vnp_OrderType,
#             vnp_ReturnUrl = self.return_url,
#             vnp_TxnRef = order_id,
#             vnp_ExpireDate = (datetime.now() + timedelta(minutes=limit_time)).strftime('%Y%m%d%H%M%S')
#         )
#         # convert dict to args
#         data_arg = payment_model.dict()
#         data_str = urllib.parse.urlencode(data_arg)
#         hash_value = self.hash.hmac_sha256(data = data_str)
#         return self.base_url + "?" + data_str + "&vnp_SecureHash=" + hash_value
        