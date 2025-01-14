import urllib.parse
from datetime import datetime, timedelta
from services.vnpay.cmd import Base
from typing import Annotated, Literal
from fastapi import Query
from config.configs import get_config
from common.models.request import OrderCreated
from services.vnpay.models.requests import PaymentModel

class OrderWooCommer(Base):
    def __init__(self, 
                 env : Annotated[Literal["sandbox", "product"], Query(description = "Select environment")],
                 from_init: bool, 
                 sandbox, 
                 product) -> None:
        super().__init__(env = env, from_init=from_init, sandbox=sandbox, product=product)
        
    def create_order(self, order_data: OrderCreated) -> str:
        __config = get_config()
        if self.env == "sandbox":
            payment_model = PaymentModel(
                vnp_Version = self.version,
                vnp_Command = 'pay',
                vnp_TmnCode = self.sandbox.terminal_code,
                vnp_Amount = order_data.amount * 100,
                vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S'),
                vnp_CurrCode = "VND",
                vnp_IpAddr = order_data.ip_address,
                vnp_Locale = order_data.locale,
                vnp_OrderInfo = order_data.description,
                vnp_OrderType = "billpayment",
                vnp_ReturnUrl = __config.get_config('PAYMENT_RETURN'),
                vnp_TxnRef = order_data.order_id,
                vnp_ExpireDate = (datetime.now() + timedelta(minutes=order_data.limit_time)).strftime('%Y%m%d%H%M%S')
            )
            data_arg = payment_model.dict()
            data_str = urllib.parse.urlencode(data_arg)
            hash_value = self.sandbox.hash_data(data = data_str)
            return self.url_sandbox + "?" + data_str + "&vnp_SecureHash=" + hash_value
        else:
            pass
        
        return 'Order created'