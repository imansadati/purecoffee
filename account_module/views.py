from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from account_module.helper import *
from .forms import RegisterForm, OtpForm, LoginForm, ForgotPasswordForm
from .models import User
from utils.check_unauthenticated_user import UnauthenticatedRequiredMixin


class RegisterView(UnauthenticatedRequiredMixin, View):

    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_mobile = register_form.cleaned_data.get('phone_number')
            user_password = register_form.cleaned_data.get('password')
            user_full_name = register_form.cleaned_data.get('full_name')

            user: User = User.objects.filter(phone_number__iexact=user_mobile).first()
            if user:
                register_form.add_error('phone_number', 'شماره موبایل وارد شده تکراری می باشد')
            else:
                _otp = get_random_otp()
                new_user = User(
                    full_name=user_full_name,
                    phone_number=user_mobile,
                    otp=_otp,
                    email=user_email,
                    is_active=False,
                    username=user_mobile)
                new_user.set_password(user_password)
                new_user.save()
                send_otp(user_mobile, otp=_otp)
                request.session['otp'] = _otp
                request.session['phone_number'] = user_mobile
                return redirect(reverse('verify_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class ResendOtpView(UnauthenticatedRequiredMixin, View):
    def get(self, request: HttpRequest):
        mobile = request.session.get('phone_number')
        _otp = get_random_otp()
        user: User = User.objects.filter(phone_number__iexact=mobile).first()
        user.otp = _otp
        user.save()
        send_otp(mobile, _otp)
        request.session['otp'] = _otp
        return redirect(reverse('verify_page'))


class VerifyView(UnauthenticatedRequiredMixin, View):
    def get(self, request):
        otp_form = OtpForm()
        context = {
            'otp_form': otp_form
        }
        return render(request, 'account_module/verify.html', context)

    def post(self, request: HttpRequest):
        otp_form = OtpForm(request.POST)
        if otp_form.is_valid():
            mobile = request.session.get('phone_number')
            user: User = User.objects.filter(phone_number__iexact=mobile).first()
            otp = otp_form.cleaned_data.get('otp')
            stored_otp = user.otp
            if check_otp_expiration(user.otp_create_time):
                if int(otp) == int(stored_otp):
                    if not user.is_active:
                        user.is_active = True
                        user.save()
                        login(request, user)
                        return redirect(reverse('user_dashboard'))
                    otp_form.add_error('otp', 'در ثبت نام اشتباهی رخ داده است')
                    return redirect(reverse('register_page'))
                otp_form.add_error('otp', 'کد تایید اشتباه می باشد')
            else:
                otp_form.add_error('otp', 'زمان استفاده از کد تایید تمام شده است')

        context = {
            'otp_form': otp_form
        }
        return render(request, 'account_module/verify.html', context)


class LoginView(UnauthenticatedRequiredMixin, View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_mobile = login_form.cleaned_data.get('phone_number')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(phone_number__iexact=user_mobile).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('phone_number', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('user_dashboard'))
                    else:
                        login_form.add_error('password', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('phone_number', 'کاربری با مشخصات وارد شده یافت نشد')
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse('login_page'))


class ForgotPasswordView(UnauthenticatedRequiredMixin, View):
    def get(self, request):
        forgot_form = ForgotPasswordForm()
        context = {
            'forgot_form': forgot_form
        }
        return render(request, 'account_module/forgot.html', context)

    def post(self, request: HttpRequest):
        forgot_form = ForgotPasswordForm(request.POST)
        if forgot_form.is_valid():
            user_mobile = forgot_form.cleaned_data.get('phone_number')
            user: User = User.objects.filter(phone_number__iexact=user_mobile, is_active=True).first()
            if user:
                if handle_ban_request(user.id):
                    _otp = get_random_otp()
                    user.otp = _otp
                    user.otp_create_time = datetime.datetime.now()
                    user.save()
                    send_otp(user_mobile, otp=_otp)
                    request.session['otp'] = _otp
                    request.session['phone_number'] = user_mobile
                    return redirect(reverse('verify_forgot_page'))
                forgot_form.add_error('phone_number', 'بیش از حد درخواست داده اید. لطفا بعدا تلاش کنید')
            else:
                forgot_form.add_error('phone_number', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'forgot_form': forgot_form
        }
        return render(request, 'account_module/forgot.html', context)


class VerifyForgot(UnauthenticatedRequiredMixin, View):
    def get(self, request):
        otp_form = OtpForm()
        context = {
            'otp_form': otp_form
        }
        return render(request, 'account_module/forgot_verify.html', context)

    def post(self, request: HttpRequest):
        otp_form = OtpForm(request.POST)
        if otp_form.is_valid():
            user_mobile = request.session.get('phone_number')
            user_otp = otp_form.cleaned_data.get('otp')
            user: User = User.objects.filter(phone_number__iexact=user_mobile, is_active=True).first()
            stored_otp = user.otp
            if check_otp_expiration(user.otp_create_time):
                if int(user_otp) == int(stored_otp):
                    user.save()
                    login(request, user)
                    return redirect(reverse('home_page'))
                otp_form.add_error('otp', 'کد تایید اشتباه می باشد. لطفا صحیح وارد کنید')
            else:
                otp_form.add_error('otp', 'زمان استفاده از کد تایید تمام شده است')

        context = {
            'otp_form': otp_form,
        }
        return render(request, 'account_module/forgot_verify.html', context)
