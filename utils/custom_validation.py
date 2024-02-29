from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_iranian_phone(value):
    cleaned_value = ''.join(filter(str.isdigit, value))

    if len(cleaned_value) != 11:
        raise ValidationError(
            _('شماره موبایل وارد شده را با فرمت صحیح وارد کنید'),
            code='invalid'
        )

    if not cleaned_value.startswith('09'):
        raise ValidationError(
            _('شماره موبایل وارد شده را با فرمت صحیح وارد کنید'),
            code='invalid'
        )
