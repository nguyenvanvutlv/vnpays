# vnpays

- Cổng thanh toán VNPAY sử dụng python. Tích hợp vào web bán hàng (thương mại điện tử)

# TÍNH NĂNG

- ✅ MÔI TRƯỜNG DEV sử dụng django: tạo thanh toán, nhận kết quả thanh toán

- ✨ MÔI TRƯỜNG PRODUCT sử dụng fastapi [đang cập nhật]

# TÀI LIỆU API VNPAY

- ✅ Phiên bản hiện tại: 2.1.0  

- ✅ Môi trường sandbox: [VNPAY SANDBOX](https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html)

- ✏️ Môi trường thực tế: [Đang cập nhật]

# YÊU CẦU DỰ ÁN

- Python >= 3.10
- Docker
- MySQL
- [Kiến thức về mã hóa Hashing]


# DỮ LIỆU KHÁCH HÀNG KHI THANH TOÁN

```txt
order_id: Mã hóa đơn
amount: Số tiền thanh toán (nhân với 100, khớp dữ liệu với vnpay)
ip_address: Địa chỉ ip khách hàng
order_info: Mô tả về mặt hàng
```

# CẤU HÌNH NHẬN DỮ LIỆU TỪ VNPAY

## MẶC ĐỊNH

- ✏️ [updating]

## TÙY CHỈNH

- ✏️ [updating]


```.env
SECRET_KEY_VNPAY=
CODE_VNPAY=
```
