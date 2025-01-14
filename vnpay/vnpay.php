<?php
/**
 * Plugin Name: CÔNG THANH TOÁN VNPAY
 * Description: TÍCH HỢP CỔNG THANH TOÁN VNPAY VÀO TRANG WEB THƯƠNG MẠI ĐIỆN TỬ
 * Version: 2.1.0
 * Author: VU NGUYEN VAN
 * Author URI: https://vnpay.vn/
 * Text Domain: wc-vnpay-pay
 * 
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'plugins_loaded', 'init_vnpay_pay_gateway' );
function init_vnpay_pay_gateway() {
    if ( ! class_exists( 'WC_Payment_Gateway' ) ) {
        return;
    }
    require_once plugin_dir_path( __FILE__ ) . 'includes/class-wc-gateway-vnpay-method-defauft.php';

    add_filter( 'woocommerce_payment_gateways', 'add_vnpay_pay_gateway' );
    function add_vnpay_pay_gateway( $gateways ) {
        $gateways[] = 'WC_Gateway_VNPAY_Method_Defauft';
        return $gateways;
    }
}
