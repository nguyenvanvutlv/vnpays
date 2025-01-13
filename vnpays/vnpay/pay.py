from vnpay import SingletonMeta
from datetime import datetime, timedelta
from vnpay.models.requests import PaymentModel
from vnpay.models.response import PaymentResponse
from vnpay.hash import Hashing
import urllib.parse


class VNPAY(metaclass = SingletonMeta):
    def __init__(self, 
                 base_url: str, 
                 return_url: str,
                 version: str, 
                 terminal_code: str,
                 secret_key: str
                 ) -> None:
        self.base_url = base_url
        self.return_url = return_url
        self.version = version
        self.terminal_code = terminal_code
        self.hash = Hashing(secret_key = secret_key)
        
        
    def change_url(self, base_url: str, version: str, terminal_code: str) -> None:
        self.base_url = base_url
        self.version = version
        self.terminal_code = terminal_code
        
    def validate_payment(self, data: PaymentResponse) -> bool:
        data_dict = data.dict()
        vnp_SecureHash = data_dict.pop('vnp_SecureHash')
        data_str = urllib.parse.urlencode(data_dict)
        hash_value = self.hash.hmac_sha256(data = data_str)
        return hash_value == vnp_SecureHash
        
        
    def create_payment(self, order_id: str, 
                       vnp_Amount: int, 
                       vnp_IpAddr: str,
                       vnp_OrderInfo : str,
                       limit_time: int = 15,
                       vnp_OrderType : str = 'billpayment',
                       vnp_Locale : str = 'vn',
                       vnp_CurrCode: str = "VND",
                       ) -> str:
        vnp_OrderInfo = urllib.parse.quote_plus(vnp_OrderInfo)
        payment_model = PaymentModel(
            vnp_Version = self.version,
            vnp_Command = 'pay',
            vnp_TmnCode = self.terminal_code,
            vnp_Amount = vnp_Amount,
            vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S'),
            vnp_CurrCode = vnp_CurrCode,
            vnp_IpAddr = vnp_IpAddr,
            vnp_Locale = vnp_Locale,
            vnp_OrderInfo = vnp_OrderInfo,
            vnp_OrderType = vnp_OrderType,
            vnp_ReturnUrl = self.return_url,
            vnp_TxnRef = order_id,
            vnp_ExpireDate = (datetime.now() + timedelta(minutes=limit_time)).strftime('%Y%m%d%H%M%S')
        )
        # convert dict to args
        data_arg = payment_model.dict()
        data_str = urllib.parse.urlencode(data_arg)
        hash_value = self.hash.hmac_sha256(data = data_str)
        return self.base_url + "?" + data_str + "&vnp_SecureHash=" + hash_value
        