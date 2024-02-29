import datetime

import pytz


def check_order_detail_expiration(order_create_added):
    iran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.datetime.now(iran_tz)
    otp_time = order_create_added
    diff_time = now - otp_time
    print(diff_time)

    if diff_time.seconds > 3:
        return False
    return True
