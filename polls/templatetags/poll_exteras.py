from django import template
from jalali_date import date2jalali, datetime2jalali
from jdatetime import datetime as jdatetime_datetime

register = template.Library()


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    if value:
        jalali_date = jdatetime_datetime.fromgregorian(
            year=value.year,
            month=value.month,
            day=value.day,
        )
        return jalali_date.strftime('%d %B %Y')
    else:
        return None


@register.filter(name='show_jalali_date_time')
def jalali_datetime(value):
    # jalali_date = jdatetime_datetime.fromgregorian(
    #     year=value.year,
    #     month=value.month,
    #     day=value.day,
    #     hour=value.hour,
    #     minute=value.minute,
    #     second=value.second
    # )
    # return jalali_date.strftime('%d %B %Y - %H:%M:%S')
    if value:
        jalali_date = jdatetime_datetime.fromgregorian(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.second
        )
        return jalali_date.strftime('%d %B %Y - %H:%M:%S')
    else:
        return ''


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return '{:,}'.format(value) + ' تومان'
