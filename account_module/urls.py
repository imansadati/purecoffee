from django.urls import path

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('verify', views.VerifyView.as_view(), name='verify_page'),
    path('resend-otp-code', views.ResendOtpView.as_view(), name='resend_otp_code'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('verify-forgot-password', views.VerifyForgot.as_view(), name='verify_forgot_page'),
    path('logout', views.logout_user, name='logout_user'),
]
