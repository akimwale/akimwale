from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('chat/', views.chatter, name='chatter'),
    path('predefined-messages/', views.predefined_messages, name='predefined_messages'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/unread/<int:notification_id>/', views.mark_as_unread, name='mark_as_unread'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('recovery/', views.purchase_recovery_key, name='recovery'),
    path('digital/', views.keys, name='digital'),
    path('payment/<int:pk>/', views.payment_page, name='payment_page'),
    path('crypto-payment/<int:pk>/', views.crypto_payment, name='crypto_payment'),
    path('gift_card_payment/<int:pk>/', views.gift_card_payment, name='gift_card_payment'),
    path('mobile-payment/', views.mobile_bank, name='mobile_payment'),
    path('bank-transfer-payment/', views.transfer_redirect, name='bank_transfer_payment'),
    path('get-social-apps/<int:profile_id>/', views.get_social_apps, name='get_social_apps'),
    path('create-payment/<int:digital_key_id>/', views.create_payment, name='create_payment'),
    path('success/', views.success, name='success'),
    path('crypto-prices/', views.crypto_prices, name='crypto_prices'),
    path('converter/', views.crypto_converter, name='crypto_converter'),
    path('accounts/convert/', views.convert_crypto, name='convert'),
    path('purchase/', views.purchase_page, name='purchase_page'),
    path('process-purchase', views.process_payment, name='process_purchase'),
    path('checkout/', views.checkout, name='checkout'),
    path('cancel/', views.cancel, name='cancel'),
    path('crypto-dashboard/', views.crypto_dashboard, name='crypto_dashboard'),
    path('portfolio/', views.portfolio_view, name='portfolio_view'),
    path('deposit/', views.deposit, name='deposit'),
    path('portfolio/deposit/', views.deposit_view, name='deposit_view'),
    path('portfolio/withdraw/', views.withdrawal_view, name='withdrawal_view'),
]