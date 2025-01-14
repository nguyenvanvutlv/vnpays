<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WC_Gateway_VNPAY_Method_Defauft extends WC_Payment_Gateway {
    private $api_url;

    public function __construct() {
        $current_language = get_locale();

        $this->id                 = 'vnpay_pay_defauft';
        $this->icon = plugins_url('assets/images/vnpay_logo.png', dirname(__FILE__));
        $this->has_fields         = false;

        $this->method_title       = __( $current_language == 'vi' ? 'VNPAY - Cổng thanh toán VNPAY-QR (mặc định)' : 'VNPAY - Default Payment Method', 'wc-vnpay-pay' );
        $this->method_description = __( $current_language == 'vi' ? 'Thực hiện quét Qr Code, nhập thông tin tài khoản ngân hàng (internet banking), nhập số thẻ (ATM) hoặc nhập thẻ quốc tế thanh toán' : 'scan Qr Code to pay, Enter Bank Account information (internet banking), enter card number (ATM) and enter international cards for payment', 'wc-vnpay-pay' );

        $this->init_form_fields();
        $this->init_settings();

        $environment = $this->get_option('environment');
        $this->api_url = ($environment === 'production') 
            ? 'https://pay.vnpay.vn/vpcpay.html'
            : 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html';

        $this->title        = $this->get_option( 'title' );
        $this->description  = $this->get_option( 'description' );
        $this->clientSecret = $this->get_option( 'clientSecret' );
        $this->tmnCode = $this->get_option( 'tmnCode' );
        $this->secretKey = $this->get_option( 'secretKey' );
        $this->order_status_after_payment = $this->get_option( 'order_status_after_payment' );

        add_action( 'woocommerce_update_options_payment_gateways_' . $this->id, array( $this, 'process_admin_options' ) );
        add_action( 'woocommerce_api_vnpay_pay_defauft_ipn', array( $this, 'handle_vnpay_pay_defauft_ipn' ) );
        add_action( 'woocommerce_api_vnpay_pay_defauft_return', array( $this, 'handle_vnpay_pay_defauft_return' ) );
    }

    public function init_form_fields() {
        $current_language = get_locale();

        $this->form_fields = array(
            'enabled' => array(
                'title'   => __( $current_language == 'vi' ? 'kích hoạt/Tắt' : 'Enable/Disable', 'wc-vnpay-pay' ),
                'type'    => 'checkbox',
                'label'   => __( $current_language == 'vi' ? 'Kích hoạt Cổng thanh toán VNPAY-QR' : 'Enable VNPAY Payment Gateway', 'wc-vnpay-pay' ),
                'default' => 'yes',
            ),
            'title' => array(
                'title'       => __( $current_language == 'vi' ? 'Tiêu đề phương thức thanh toán' : 'Payment Method Title', 'wc-vnpay-pay' ),
                'type'        => 'text',
                'description' => __( $current_language == 'vi' ? ' Cài đặt tiêu đề được hiển thị cho người dùng khi chọn phương thức thanh toán' : 'The title displayed to users when selecting a payment method', 'wc-vnpay-pay' ),
                'default'     => __( $current_language == 'vi' ? 'Cổng thanh toán VNPAY-QR' : 'Default Payment Method', 'wc-vnpay-pay' ),
            ),
            'description' => array(
                'title'       => __( $current_language == 'vi' ? 'Mô tả phương thức thanh toán' : 'Payment Method Description', 'wc-vnpay-pay' ),
                'type'        => 'textarea',
                'description' => __( $current_language == 'vi' ? 'Cài đặt mô tả phương thức thanh toán qua Cổng thanh toán VNPAY-QR' : 'Set the payment method descriptiont', 'wc-vnpay-pay' ),
                'default'     => __( $current_language == 'vi' ? 'Chọn phương thức thanh toán bằng ATM, tài khoản ngân hàng nội địa' : 'Choose a payment method using a bank account or domestic card', 'wc-vnpay-pay' ),
            ),
            'environment' => array(
            'title'          => __( $current_language == 'vi' ? 'Môi trường kết nối' : 'Payment Environment', 'vnpay'),
            'type'           => 'select',
            'description'    => $current_language == 'vi' ? 'Chọn môi trường kiểm thử hoặc thanh toán thật' : 'Select the testing environment or the production payment environment',
            'options'        => array(
                'sandbox'    => __( $current_language == 'vi' ? 'Môi trường kiểm thử' : 'Sandbox', 'vnpay'),
                'production' => __( $current_language == 'vi' ? 'Môi trường thật' : 'Production', 'vnpay'),
            ),
            'default' => 'sandbox',
        ),
            'tmnCode' => array(
                'title'       => __( 'Terminal code', 'wc-vnpay-pay' ),
                'type'        => 'text',
                'description' => $current_language == 'vi' ? 'Mã định danh kết nối do VNPAY cung cấp' : 'The terminal code is provided by VNPAY',
            ),
            'secretKey' => array(
                'title'       => __( 'Secret key', 'wc-vnpay-pay' ),
                'type'        => 'text',
                'description' => $current_language == 'vi' ? 'Chuỗi bí mật để xác thực và mã hóa dữ liệu do VNPAY cung cấp. Vui lòng, bảo mật thông tin này'
                : 'The secret string for authentication and data encryption is provided by VNPAY. Please keep this information secure',
            ),
            'order_status' => array(
                'title'          => __( $current_language == 'vi' ? 'Trạng thái đơn hàng sau thanh toán' : 'Order status after payment', 'wc-vnpay-pay' ),
                'type'           => 'select',
                'description'    => $current_language == 'vi' ? 'Chọn trạng thái đơn hàng sau khi khách hàng thanh toán thành công' : 'Select the order status after successful payment',
                'default'        => 'completed',
                'options'        => array(
                    'processing' => $current_language == 'vi' ? 'Đang xử lý' : 'processing',
                    'completed'  => $current_language == 'vi' ? 'Hoàn Thành' : 'completed',
                ),
            ),
            'locale' => array(
                'title'       => __( $current_language == 'vi' ? 'Ngôn ngữ' : 'Locale', 'wc-vnpay-pay' ),
                'type'        => 'select',
                'description' => $current_language == 'vi' ? 'Chọn ngôn ngữ hiển thị cho trang thanh toán' : 'Select the display language for the payment page',
                'default'     => 'vn',
                'options'     => array(
                    'vn'      => 'Tiếng Việt',
                    'en'      => 'English',
                ),
            ),
        );
    }

    public function get_icon() {
        $icon = '';
        if ($this->icon) {
            $icon .= '<img src="' . esc_url($this->icon) . '" alt="Logo" style="width: 60px; height: auto; margin-right: 10px;" />';
        }
        return $icon;
    }

    public function process_payment( $order_id ) {
        date_default_timezone_set('Asia/Ho_Chi_Minh');
        $order = wc_get_order( $order_id );

        $tmnCode = $this->get_option('tmnCode');
        $locale = $this->get_option('locale');
        $secretKey = $this->get_option('secretKey');

        $orderReference = $order->get_order_number();
        $orderInfo = 'init Order-woocommerce-vnpay-pay-defauft:' . $orderReference;
        $amount = $order->get_total() * 100;
        $currCode = $order->get_currency();
        //error_log('currCode: ' . $currCode);

        $currCode = $order->get_currency();
        if ($currCode !== 'VND') {
            if ($locale === 'vn') {
                wc_add_notice(__('Chỉ hỗ trợ thanh toán bằng VND. Vui lòng chọn hình thức thanh toán khác', 'vnpay'), 'error');
            }
            else {
                wc_add_notice(__('This VNPAY payment gateway only supports VND currency. Please select a different payment method', 'vnpay'), 'error');
            }
            wp_redirect(wc_get_cart_url());
            exit;
        }

        $returnUrl = site_url('/wc-api/vnpay_pay_defauft_return/');
        //error_log('returnUrl: ' . $returnUrl);
        $createDate = date('YmdHis');
        $expiryDate = date('YmdHis', strtotime('+15 minutes'));
        $ipAddr = $_SERVER['REMOTE_ADDR'];

        $inputData = array(
            "vnp_TmnCode"       => $tmnCode,
            "vnp_Amount"        => $amount,
            "vnp_Command"       => 'pay',
            "vnp_CreateDate"    => $createDate,
            "vnp_ExpireDate"    => $expiryDate,
            "vnp_CurrCode"      => $currCode,
            "vnp_IpAddr"        => $ipAddr,
            "vnp_Locale"        => $locale,
            "vnp_OrderInfo"     => $orderInfo,
            "vnp_OrderType"     => 'other',
            "vnp_ReturnUrl"     => $returnUrl,
            "vnp_TxnRef"        => $orderReference,
            "vnp_Version"       => '2.1.0',
        );
        ksort($inputData);
        $queryString = '';
    
        foreach ($inputData as $key => $value) {
            $encodedValue = urlencode($value);
            $queryString .= $key . '=' . $encodedValue . '&';
        }
        $queryString = rtrim($queryString, '&');
        //error_log('queryString: ' . $queryString);
        //error_log('secretKey: ' . $secretKey);
        $secureHash = hash_hmac('sha512', $queryString, $secretKey);

        if (isset($secretKey) && isset($secureHash))  {

            $payment_redirect_url = $this->api_url . '?' . $queryString . '&vnp_SecureHash=' . $secureHash;
        }

        $order->update_status('on-hold');
        //error_log('payment_redirect_url ' . $payment_redirect_url);
        return array(
            'result' => 'success',
            'redirect' => $payment_redirect_url,
        );
        
    }


    public function handle_vnpay_pay_defauft_ipn() {
        global $woocommerce;
        try {
            $data = $_GET;
            $returnData = array();
            $params = array();
            $secretKey = $this->get_option('secretKey');

            if (empty($data) || count($data) === 0) {
                $returnData['RspCode'] = '99';
                $returnData['Message'] = 'No data';
                echo json_encode($returnData);
                exit();
            }

            foreach ($data as $key => $value) {
                if (substr($key, 0, 4) == "vnp_") {
                    $params[$key] = $value;
                }
            }

            $vnp_TxnRef = isset($data["vnp_TxnRef"]) ? $data["vnp_TxnRef"] : null;
            if ($vnp_TxnRef === null) {
                $returnData['RspCode'] = '01';
                $returnData['Message'] = 'Invalid transaction Id';
                echo json_encode($returnData);
                exit();
            }

            $order_id = intval($vnp_TxnRef);
            $order = wc_get_order($order_id);
            if ($order === false) { 
                $returnData['RspCode'] = '01';
                $returnData['Message'] = 'Order not found';
                echo json_encode($returnData);
                exit();
            }


            $vnp_Amount = isset($params['vnp_Amount']) ? floatval($params['vnp_Amount']) : 0;
            $orderTotal = $order->get_total() * 100;
            if ($vnp_Amount != $orderTotal) {
                $returnData['RspCode'] = '04';
                $returnData['Message'] = 'Invalid amount';
                echo json_encode($returnData);
                exit();
            }

            if (!isset($params['vnp_SecureHash'])) {
                $returnData['RspCode'] = '99';
                $returnData['Message'] = 'SecureHash not found';
                echo json_encode($returnData);
                exit();
            }
            $vnp_SecureHash = $params['vnp_SecureHash'];
            
            unset($params['vnp_SecureHashType']);
            unset($params['action']);
            unset($params['type']);
            unset($params['vnp_SecureHash']);
            ksort($params);
            $i = 0;
            $hashData = "";

            foreach ($params as $key => $value) {
                if ($i == 1) {
                    $hashData = $hashData . '&' . urlencode($key) . "=" . urlencode($value);
                } else {
                    $hashData = $hashData . urlencode($key) . "=" . urlencode($value);
                    $i = 1;
                }
            }

            $secureHash = hash_hmac('SHA512', $hashData, $secretKey);
            //error_log('hashData: ' . $hashData);
            //error_log('secretKey: ' . $secretKey);

            if ($order) {
                if ($secureHash === $vnp_SecureHash) {
                    if ($order->get_status() === 'on-hold') {
                        if ($params['vnp_ResponseCode'] === '00') {
                            $order->update_status($this->get_option('order_status'));
                            $order->add_order_note(__('Payment confirmed successfully', 'woocommerce'));
                            $returnData['RspCode'] = '00';
                            $returnData['Message'] = 'Confirm Success';
                        } else {
                            $order->update_status('failed');
                            $order->add_order_note(__('Payment failed', 'woocommerce'));
                            $returnData['RspCode'] = '00';
                            $returnData['Message'] = 'Confirm Success';
                        }
                    } else {
                        $returnData['RspCode'] = '02';
                        $returnData['Message'] = 'Order already confirmed';
                    }
                } else {
                    $returnData['RspCode'] = '97';
                    $returnData['Message'] = 'Invalid checksum';
                }
            } else {
                $returnData['RspCode'] = '01';
                $returnData['Message'] = 'Order not found';
            }
        }
        catch (Exception $e) {
            $returnData['RspCode'] = '98';
            $returnData['Message'] = 'An error occurred: ' . $e->getMessage();
        }
        echo json_encode($returnData);
        exit();
    }

    public function handle_vnpay_pay_defauft_return() {
        $locale = $this->get_option('locale');
        try {
            $data = $_GET;
            $returnData = array();
            $params = array();
            $secretKey = $this->get_option('secretKey');

            foreach ($data as $key => $value) {
                if (substr($key, 0, 4) == "vnp_") {
                    $params[$key] = $value;
                }
            }

            $vnp_TxnRef = isset($data["vnp_TxnRef"]) ? $data["vnp_TxnRef"] : null;
            if ($vnp_TxnRef === null) {
				if ($locale ==='vn') {
					 $message = 'Mã đơn hàng thanh toán không hợp lệ. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ.';
				}
				else {
					$message = 'The transaction Id is not found. Please contact the Customer Service team of the payment website for assistance.';
				}
                WC()->session->set('payment_message', $message);
                wp_redirect($this->get_return_url($order));
                exit;
            }

            $order_id = intval($vnp_TxnRef);
            $order = wc_get_order($order_id);
            if ($order === false) { 
				if ($locale ==='vn') {
					 $message = 'Không tìm thấy đơn hàng thanh toán. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ.';
				}
				else {
					$message = 'The Order Id is not found. Please contact the Customer Service team of the payment website for assistance.';
				}
                WC()->session->set('payment_message', $message);
                wp_redirect($this->get_return_url($order));
                exit;
            }


            $vnp_Amount = isset($params['vnp_Amount']) ? floatval($params['vnp_Amount']) : 0;
            $orderTotal = $order->get_total() * 100;
            if ($vnp_Amount != $orderTotal) {
				if ($locale ==='vn') {
					 $message = 'Số tiền thanh toán không hợp lệ. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ';
				}
				else {
					$message = 'The amount is invalid. Please contact the Customer Service team of the payment website for assistance.';
				}
                WC()->session->set('payment_message', $message);
                wp_redirect($this->get_return_url($order));
                exit;
            }

            $vnp_SecureHash = $params['vnp_SecureHash'];
            
            unset($params['vnp_SecureHashType']);
            unset($params['action']);
            unset($params['type']);
            unset($params['vnp_SecureHash']);
            ksort($params);
            $i = 0;
            $hashData = "";

            foreach ($params as $key => $value) {
                if ($i == 1) {
                    $hashData = $hashData . '&' . urlencode($key) . "=" . urlencode($value);
                } else {
                    $hashData = $hashData . urlencode($key) . "=" . urlencode($value);
                    $i = 1;
                }
            }

            $secureHash = hash_hmac('SHA512', $hashData, $secretKey);

            if ($secureHash != $vnp_SecureHash) {
				if ($locale ==='vn') {
					 $message = 'Chữ ký giao dịch không hợp lệ. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ.';
				}
				else {
					$message = 'Invalid checksum. Please contact the Customer Service team of the payment website for assistance.';
				}
                WC()->session->set('payment_message', $message);
                wp_redirect($this->get_return_url($order));
                exit();
            }

            if ($order) {
                if ($secureHash === $vnp_SecureHash) {
                    if ($params['vnp_ResponseCode'] === '00'){
                        if ($locale ==='vn') {
                            $message = 'Bạn đã thanh toán thành công qua Cổng thanh toán VNPAY-QR. Cảm ơn bạn đã sử dụng dịch vụ!';
                        }
                        else {
                            $message = 'The order is successful. Thanks!';
                        }
                        WC()->session->set('payment_message', $message);
                    } elseif ($params['vnp_ResponseCode'] === '24') {
                        if ($locale ==='vn') {
                            $message = 'Bạn đã hủy giao dịch qua Cổng thanh toán VNPAY-QR. 
                            Nếu có vấn đề gì trong quá trình thanh toán mà không thể hoàn tất. Xin vui lòng liên hệ Hotline CSKH của VNPAY để được hỗ trợ. 
                            Hotline: 1900 55 55 77 Email: hotrovnpay@vnpay.vn
                            ';
                        }
                        else {
                            $message = 'You have canceled the transaction via VNPAY Payment Gateway.
                            If you encountered any issues during the payment process and were unable to complete it, please contact VNPAY Customer Service Hotline for assistance.
                            Hotline: 1900 55 55 77 Email: hotrovnpay@vnpay.vn
                            ';
                        }
                        WC()->session->set('payment_message', $message);
                    }
                     else {
                        if ($locale ==='vn') {
                            $message = 'Giao dịch thanh toán không thành công qua Cổng thanh toán VNPAY-QR. 
                            Nếu gặp lỗi trong quá trình thanh toán. Xin vui lòng liên hệ Hotline CSKH của VNPAY để được hỗ trợ.
                            Hotline: 1900 55 55 77 Email: hotrovnpay@vnpay.vn
                            ';
                        }
                        else {
                            $message = 'The payment transaction was unsuccessful through the VNPAY Payment Gateway.
                            If you encountered any errors during the payment process, please contact VNPAY Customer Service Hotline for assistance.
                            Hotline: 1900 55 55 77 Email: hotrovnpay@vnpay.vn
                            ';
                        }
                        WC()->session->set('payment_message', $message);
                    }
                    wp_redirect($this->get_return_url($order));
                    exit();

                } else {
                    if ($locale ==='vn') {
                        $message = 'Có lỗi trong quá trình xử lý, sai chữ ký. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ.';
                    }
                    else {
                        $message = 'There was an error during processing due to an invalid signature. Please contact the Customer Service team of the payment website for assistance.';
                    }
                    WC()->session->set('payment_message', $message);
                    wp_redirect($this->get_return_url($order));
                    exit();
                }
            } else {
                if ($locale ==='vn') {
                    $message = 'Có lỗi trong quá trình xử lý, không tìm thấy đơn hàng. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ.';
                }
                else {
                    $message = 'There was an error during processing, and the order could not be found. Please contact the Customer Service team of the payment website for assistance.';
                }
                WC()->session->set('payment_message', $message);
                wp_redirect($this->get_return_url($order));
                exit();
            }
        }
        catch (Exception $e) {
            if ($locale ==='vn') {
                $message = 'Có lỗi trong quá trình xử lý. Vui lòng liên hệ bộ phận CSKH của website thanh toán để được hỗ trợ.';
            }
            else {
                $message = 'There was an error during processing. Please contact the Customer Service team of the payment website for assistance.';
            }
            WC()->session->set('payment_message', $message);
            wp_redirect($this->get_return_url($order));
            exit();
        }
    }

}

function display_vnpay_pay_defauft_payment_message($order_id) {
    $message = WC()->session->get('payment_message');
    if ($message) {
        echo '<div class="woocommerce-message">' . esc_html($message) . '</div>';
        WC()->session->__unset('payment_message');
    }
}

add_action('woocommerce_thankyou', 'display_vnpay_pay_defauft_payment_message');

