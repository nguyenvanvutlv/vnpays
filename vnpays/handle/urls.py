from django.urls import path
from handle.views import home, payment, payment_return, payment_ipn


urlpatterns = [
    path('', home, name='home'),
    path('payment', payment, name='payment'),
    path('ReturnUrl', payment_return, name='payment_return'),
    path('IPN', payment_ipn, name='payment_ipn'),
]
