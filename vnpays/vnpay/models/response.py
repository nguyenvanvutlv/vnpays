from typing import Literal
from pydantic import BaseModel, Field


class PaymentResponse(BaseModel):
    vnp_Amount: int = Field(..., title="Số tiền thanh toán")
    vnp_BankCode: str = Field(..., title="Mã ngân hàng")
    vnp_BankTranNo: str = Field(..., title="Mã giao dịch ngân hàng")
    vnp_CardType: str = Field(..., title="Loại thẻ")
    vnp_OrderInfo: str = Field(..., title="Thông tin đơn hàng")
    vnp_PayDate: str = Field(..., title="Ngày thanh toán")
    vnp_ResponseCode: str = Field(..., title="Mã phản hồi")
    vnp_TmnCode: str = Field(..., title="Mã cửa hàng")
    vnp_TransactionNo: str = Field(..., title="Mã giao dịch")
    vnp_TransactionStatus: str = Field(..., title="Trạng thái giao dịch")
    vnp_TxnRef: str = Field(..., title="Mã tham chiếu")
    vnp_SecureHash: str = Field(..., title="Băm bảo mật")
    
    def dict(self) -> dict:
        return self.model_dump()