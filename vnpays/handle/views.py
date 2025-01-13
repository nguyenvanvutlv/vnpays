from django.shortcuts import render, redirect
from handle.forms import PaymentForm
from django.conf import settings
from vnpay.pay import VNPAY
from vnpay.models.response import PaymentResponse
# Create your views here.


def home(request) :
    return render(request, 'index.html')


def payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            amount = int(form.cleaned_data['amount']) * 100
            order_desc = form.cleaned_data['order_desc']
            ip_address = form.cleaned_data['ip_address']
            
            url : VNPAY = settings.VNPAY_SYSTEM.create_payment(
                order_id = order_id,
                vnp_Amount = amount,
                vnp_IpAddr = ip_address,
                vnp_OrderInfo = order_desc,
            )
            return redirect(url)
        else:
            return render(request, 'payment.html', {'title' : 'Tạo thanh toán'})
    else:
        return render(request, 'payment.html', {'title' : 'Tạo thanh toán'})
    
def payment_ipn(request):
    try:
        payment_response = PaymentResponse(**request.GET.dict())
        vnpay : VNPAY = settings.VNPAY_SYSTEM
        status_payment = vnpay.validate_payment(payment_response)
        assert status_payment, 'Thanh toán không hợp lệ'
        return render(request, 'index.html')
    except Exception as e:
        return render(request, 'index.html')
    
def payment_return(request):
    
    try:
        payment_response = PaymentResponse(**request.GET.dict())
        vnpay : VNPAY = settings.VNPAY_SYSTEM
        status_payment = vnpay.validate_payment(payment_response)
        assert status_payment, 'Thanh toán không hợp lệ'
        return render(request, 'payment_return.html', 
                      {'title' : 'Kết quả thanh toán',
                       'result' : 'Thanh toán thành công',
                       'order_id' : payment_response.vnp_TxnRef,
                       'amount' : payment_response.vnp_Amount // 100,
                       'order_desc' : payment_response.vnp_OrderInfo.replace('+', ' '),
                       'vnp_TransactionNo' : payment_response.vnp_TransactionNo,
                       'vnp_ResponseCode' : payment_response.vnp_ResponseCode,
                       })
    except Exception as e:
        return render(request, 'payment_return.html', 
                      {'title' : 'Kết quả thanh toán', 
                       'result' : "Thanh toán thất bại",
                       'order_id' : payment_response.vnp_TxnRef,
                       'amount' : payment_response.vnp_Amount // 100,
                       'order_desc' : payment_response.vnp_OrderInfo.replace('+', ' '),
                       'vnp_TransactionNo' : payment_response.vnp_TransactionNo,
                       'vnp_ResponseCode' : payment_response.vnp_ResponseCode,
                       'msg' : str(e)})
    