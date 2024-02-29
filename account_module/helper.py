import datetime
from random import randint
import pytz
from django.utils import timezone
from kavenegar import *
from CoffeeShop import settings
from CoffeeShop.settings import Kavenegar_API
from django.core.cache import cache


def send_otp(phone_number, otp):
    mobile = [phone_number, ]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '10008663',  # optional
            'receptor': mobile,  # multiple mobile number, split by comma
            'message': 'your otp is {}'.format(otp),
        }
        api.sms_send(params)
        print('OTP: ', otp)
        # print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(1000, 9999)


def check_otp_expiration(otp_create_time):
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.datetime.now(iran_tz)
    otp_time = otp_create_time
    diff_time = now - otp_time
    print(diff_time)

    if diff_time.seconds > settings.OTP_EXPIRATION_TIME:
        return False
    return True


def handle_ban_request(user_id):
    request_count_key = f"otp_request_count: {user_id}"
    request_count = cache.get(request_count_key, 0) + 1
    cache.set(request_count_key, request_count, timeout=3600)

    if request_count < 4:
        return True
    else:
        ban_key = f"otp_ban: {user_id}"
        ban_duration = 3600
        ban_end_time = timezone.now() + timezone.timedelta(seconds=ban_duration)
        cache.set(ban_key, True, timeout=ban_duration)
        cache.set(f"{ban_key}:expiry", ban_end_time, timeout=ban_duration)

        if timezone.now() < ban_end_time:
            return False
        cache.delete(request_count_key)

# def is_user_banned_for_otp(user_id):
#     ban_key = f'otp_ban:{user_id}'
#     ban_expiry_key = f'{ban_key}:expiry'
#     ban_expiry_time = cache.get(ban_expiry_key)
#     if ban_expiry_time is None:
#         # User is not banned
#         return False
#     elif ban_expiry_time <= timezone.now():
#         # Ban has expired
#         cache.delete_many([ban_key, ban_expiry_key])
#         return False
#     else:
#         # User is still banned
#         return True
