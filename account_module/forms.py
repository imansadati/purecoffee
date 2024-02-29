from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
import re

from django.core.validators import RegexValidator


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'نام و نام خانوادگی'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'input',
            'placeholder': 'شماره موبایل'
        })
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'placeholder': 'ایمیل (اختیاری)'
        }),
        validators=[
            validators.EmailValidator,
            validators.MaxLengthValidator(100)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'تکرار کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )

    def clean_phone_number(self):
        patterns = r'^09\d{9}$'
        phone_number = self.cleaned_data.get('phone_number')
        if re.match(patterns, phone_number):
            return phone_number
        raise ValidationError('شماره تلفن را با فرمت صحیح وارد کنید')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')


class OtpForm(forms.Form):
    otp = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'input',
            'placeholder': 'کد تایید'
        }),
    )

    def clean_otp(self):
        patterns = r'^\d{4}$'
        otp = self.cleaned_data.get('otp')
        if re.match(patterns, otp):
            return otp
        raise ValidationError('کد تایید را صحیح وارد کنید')


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'input',
            'placeholder': 'شماره موبایل'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )

    def clean_phone_number(self):
        patterns = r'^09\d{9}$'
        phone_number = self.cleaned_data.get('phone_number')
        if re.match(patterns, phone_number):
            return phone_number
        raise ValidationError('شماره تلفن را با فرمت صحیح وارد کنید')


class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'input',
            'placeholder': 'شماره موبایل'
        })
    )

    def clean_phone_number(self):
        patterns = r'^09\d{9}$'
        phone_number = self.cleaned_data.get('phone_number')
        if re.match(patterns, phone_number):
            return phone_number
        raise ValidationError('شماره تلفن را با فرمت صحیح وارد کنید')

