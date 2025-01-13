from typing import Literal
from pydantic import BaseModel, Field

class PaymentModel(BaseModel):
    vnp_Version: str = Field(description="Phiên bản thanh toán của VNPAY")
    vnp_Command: Literal['pay'] = Field(description="Loại giao dịch thanh toán")
    vnp_TmnCode: str = Field(description="Mã website tại VNPAY cho mỗi merchant")
    vnp_Amount: int = Field(description="Số tiền thanh toán")
    vnp_CreateDate: str = Field(description="Thời gian tạo giao dịch")
    vnp_CurrCode: Literal['VND'] = Field(description="Loại tiền tệ")
    vnp_IpAddr: str = Field(description="Địa chỉ IP của khách hàng thực hiện giao dịch")
    vnp_Locale: Literal['vn', 'en'] = Field(description="Ngôn ngữ giao diện thanh toán")
    vnp_OrderInfo: str = Field(description="Thông tin đơn hàng")
    vnp_OrderType: Literal['billpayment', 'topup', 'fashion', 'other'] = Field(description="Loại đơn hàng")
    vnp_ReturnUrl: str = Field(description="URL trả về sau khi thanh toán")
    vnp_ExpireDate: str = Field(description="Thời gian hết hạn giao dịch")
    vnp_TxnRef: str = Field(description="Mã giao dịch tại hệ thống của merchant")
    # vnp_SecureHash: str = Field(description="Chữ ký bảo mật của dữ liệu gửi sang VNPAY")
    
    def dict(self) -> dict:
        model_dump = self.model_dump()
        input_data = sorted(model_dump.items())
        return input_data
    
    # def add_secure_hash(self, dict_data: dict, secure_hash: str) -> dict:
    #     dict_data['vnp_SecureHash'] = secure_hash
    #     return dict_data