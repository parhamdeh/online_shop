from celery import shared_task

# local apps
from online_shop.sms_gateway.services.sms_services import SMSService


@shared_task
def send_sms(phone: str, code: int):
    data = {
        "phone":phone,
        "message": f"your verfication code is {code}"
    }
    SMSService().send_otp(data=data)

@shared_task(
    name="users.delete_inactive_users",
)
def delete_inactive_users_task():
    from online_shop.users.services.user_services import delete_inactive_users

    return delete_inactive_users()
    