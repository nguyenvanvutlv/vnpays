from typing import Annotated, Literal
from fastapi import APIRouter, Request, Query, Depends, status
from common.models import PayLoadModel
from common.models.request import OrderCreated
from services.vnpay import getVNPayService, VNPAYs
from services.vnpay.models.response import PaymentResponse

router = APIRouter(tags=["VNPAY"])


@router.post("/create_payment", response_model=PayLoadModel[str])
def create_payment(request: Request,
                   order_data: OrderCreated,
                   vnpay_service: VNPAYs = Depends(getVNPayService)
                   ) -> PayLoadModel[str]:
    service = vnpay_service.payment(env = "sandbox")
    url = service.create_order(order_data)
    
    return PayLoadModel().response(
        status_code = 200,
        message_response = 'OK',
        data = url
    )
    
@router.get("/payment_return", 
            response_model=PayLoadModel[str])
def payment_return(request: Request,
                    vnp_Amount: Annotated[int, Query(description="Số tiền thanh toán")],
                    vnp_BankCode: Annotated[str, Query(description="Mã ngân hàng")],
                    vnp_BankTranNo: Annotated[str, Query(description="Mã giao dịch ngân hàng")],
                    vnp_CardType: Annotated[str, Query(description="Loại thẻ")],
                    vnp_OrderInfo: Annotated[str, Query(description="Thông tin đơn hàng")],
                    vnp_PayDate: Annotated[str, Query(description="Ngày thanh toán")],
                    vnp_ResponseCode: Annotated[str, Query(description="Mã phản hồi")],
                    vnp_TmnCode: Annotated[str, Query(description="Mã cửa hàng")],
                    vnp_TransactionNo: Annotated[str, Query(description="Mã giao dịch")],
                    vnp_TransactionStatus: Annotated[str, Query(description="Trạng thái giao dịch")],
                    vnp_TxnRef: Annotated[str, Query(description="Mã tham chiếu")],
                    vnp_SecureHash: Annotated[str, Query(description="Băm bảo mật")],
                    vnpay_service: VNPAYs = Depends(getVNPayService)
                   ) -> PayLoadModel[str]:

    
    try:
        payment_response = PaymentResponse(
            vnp_Amount = vnp_Amount,
            vnp_BankCode = vnp_BankCode,
            vnp_BankTranNo = vnp_BankTranNo,
            vnp_CardType = vnp_CardType,
            vnp_OrderInfo = vnp_OrderInfo,
            vnp_PayDate = vnp_PayDate,
            vnp_ResponseCode = vnp_ResponseCode,
            vnp_TmnCode = vnp_TmnCode,
            vnp_TransactionNo = vnp_TransactionNo,
            vnp_TransactionStatus = vnp_TransactionStatus,
            vnp_TxnRef = vnp_TxnRef,
            vnp_SecureHash = vnp_SecureHash
        )
        assert vnpay_service.verify(payment_response), "Sai khóa bảo mật"
        
        assert payment_response.vnp_ResponseCode == '00', "Giao dịch thất bại"
        
        
        
        
        return PayLoadModel().response(
            status_code = 200,
            message_response = 'OK',
            data = 'PAYMENT SUCCESS'
        )
        
    except Exception as error:
        return PayLoadModel().response(
            status_code = status.HTTP_401_UNAUTHORIZED,
            message_response = 'ERROR',
            data = str(error)
        )