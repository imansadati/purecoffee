from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator

from account_module.models import User


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'نام و نام خانوادگی تحویل گیرنده'
        })
    )
    phone_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(regex=r'^09\d{9}$', message='شماره تلفن را با فرمت صحیح وارد کنید',
                           code='invalid_phone_number'), ],
        widget=forms.NumberInput(attrs={
            'placeholder': 'شماره موبایل'
        })
    )
    province = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'استان'
        })
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'شهر'
        })
    )
    exact_address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'آدرس دقیق'
        }),
    )
    plaque = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'placeholder': 'پلاک'
        })
    )
    postal_code = forms.IntegerField(
        required=False,
        validators=[
            RegexValidator(regex=r'^\d{10}$', message='کد پستی را با فرمت صحیح وارد کنید',
                           code='invalid_phone_number'), ],
        widget=forms.NumberInput(attrs={
            'placeholder': 'کد پستی (اختیاری)'
        })
    )


class ChangePasswordUserForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'کلمه عبور فعلی'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'کلمه عبور جدید'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ],
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'تکرار کلمه عبور جدید'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password == confirm_new_password:
            return confirm_new_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')


class CouponForm(forms.Form):
    coupon = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'درصورت وجود کد تخفیف را وارد کنید',
            'class': 'col-md-12 mt-3'
        }))
