# vnpays

- Cổng thanh toán VNPAY sử dụng python. Tích hợp vào web bán hàng (thương mại điện tử)

# TÍNH NĂNG

- ✅ MÔI TRƯỜNG DEV sử dụng django: tạo thanh toán, nhận kết quả thanh toán

- ✨ MÔI TRƯỜNG PRODUCT sử dụng fastapi [đang cập nhật]

# TÀI LIỆU API VNPAY

- ✅ Phiên bản hiện tại: 2.1.0  

- ✅ Môi trường sandbox: [VNPAY SANDBOX](https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html)

- ✏️ Môi trường thực tế: [VNPAY](https://pay.vnpay.vn/vpcpay.html)

# YÊU CẦU DỰ ÁN

- Python >= 3.10
- Docker
- MySQL
- [Kiến thức về mã hóa Hashing]


# DỮ LIỆU KHÁCH HÀNG KHI THANH TOÁN (gửi yêu cầu thanh toán)

```txt
order_id: Mã hóa đơn
amount: Số tiền thanh toán (nhân với 100, khớp dữ liệu với vnpay)
ip_address: Địa chỉ ip khách hàng
order_info: Mô tả về mặt hàng
```

- web thương mại điện tử sẽ gửi yêu cầu tạo thanh toán

+ ENDPOINT: ```https://{domain}/create_payment```
+ METHOD: ```POST```
+ PAYLOAD:

```json
{
    "order_id" : "<string> : Mã đơn hàng",
    "amount"   : "<int>    : Số tiền cần thanh toán : Định dạng số nguyên không có dấu phẩy và nhân thêm 100",
    "description" : "<string> : Mô tả thanh toán",
    "ip_address" : "<string> : Địa chỉ khách hàng thanh toán"
}
```

+ RESPONSE:

Hệ thống sẽ trả về link thanh toán, web sẽ điều hướng người dùng sang link đó

```txt
✅ url_sandbox = "https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html?{tham số thanh toán}&vnp_SecretHash={giá trị dùng cho mã hóa}"

✅ url_product = "https://pay.vnpay.vn/vpcpay.html?{tham số thanh toán}&vnp_SecretHash={giá trị dùng cho mã hóa}"
```


# CẤU HÌNH NHẬN DỮ LIỆU TỪ VNPAY (nhận thông báo thanh toán và ipn)

## MẶC ĐỊNH ✅

+ SERVICE_NAME: ```vnpays```
+ ENDPOINT: ```http://{service_name}:{port}/payment_return```
+ METHOD: ```GET```
+ PARAM_HEADER :

```
vnp_Amount: <int> - số tiền thanh toán của khách hàng
vnp_BankCode: <str> - mã tài khoản thanh toán
vnp_BankTranNo: <int> - mã giao dịch ngân hàng
vnp_CardType: <str> - loại thẻ
vnp_OrderInfo: <str> - Mô tả thanh toán - "XEM THÊM VỀ PHẦN GỬI DỮ LIỆU"
vnp_PayDate: <str> - thời gian thanh toán 'ymdhms'
vnp_ResponseCode: <str> - mã phản hồi thanh toán từ vnpay
vnp_TmnCode: <str> mã giao dịch của cửa hàng
vnp_TransactionNo: <str> mã giao dịch
vnp_TransactionStatus: <str> trạng thái giao dịch
vnp_TxnRef: <str> - mã đơn hàng - "XEM THÊM VỀ PHẦN GỬI DỮ LIỆU"
vnp_SecureHash: <str> - giá trị băm sử dụng cho việc xác thực dữ liệu
```

endpoint mặc định sẽ có phần xác thực giao dịch


## TÙY CHỈNH ✏️

+ ENDPOINT: ```https://{domain}/payment_return```
+ METHOD: ```GET```
+ PARAM_HEADER :

```
vnp_Amount: <int> - số tiền thanh toán của khách hàng
vnp_BankCode: <str> - mã tài khoản thanh toán
vnp_BankTranNo: <int> - mã giao dịch ngân hàng
vnp_CardType: <str> - loại thẻ
vnp_OrderInfo: <str> - Mô tả thanh toán - "XEM THÊM VỀ PHẦN GỬI DỮ LIỆU"
vnp_PayDate: <str> - thời gian thanh toán 'ymdhms'
vnp_ResponseCode: <str> - mã phản hồi thanh toán từ vnpay
vnp_TmnCode: <str> mã giao dịch của cửa hàng
vnp_TransactionNo: <str> mã giao dịch
vnp_TransactionStatus: <str> trạng thái giao dịch
vnp_TxnRef: <str> - mã đơn hàng - "XEM THÊM VỀ PHẦN GỬI DỮ LIỆU"
vnp_SecureHash: <str> - giá trị băm sử dụng cho việc xác thực dữ liệu
```

+ web cần có xác thực bằng thuật toán hmacsha256 trước khi cập nhật thông tin liên quan đến đơn hàng


### CẤU HÌNH CHO PHP (VIẾT PLUGIN CHO WORDPRESS)

- ✅ Plugin vnpay: cho phép thanh toán với các phương thức khác nhau (QRCODE, Quốc tế, Tài khoản ngân hàng)

### CẤU HÌNH CHO PYTHON (VIẾT SERVER TẠO THANH TOÁN)

- ✅ [BẢN LOCALHOST]

- ✏️ [BẢN SERVER]


# CẤU HÌNH GỬI YÊU CẦU HOÀN TRẢ THANH TOÁN

```.env
SECRET_KEY_VNPAY=
CODE_VNPAY=
```
