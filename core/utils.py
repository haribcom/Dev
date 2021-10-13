import logging
from functools import wraps

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import PermissionDenied

LOGGER = logging.getLogger(__name__)


def update_password(user, password):
    user.set_password(password)
    user.save()
    LOGGER.info("User Password Updated Successfully %s", user)


def send_email(**kwargs):
    subject = kwargs.get('subject', 'this is subject')
    message = kwargs.get('message', 'this is body')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = kwargs.get('recipient') if type(kwargs.get('recipient')) == list else [kwargs.get('recipient')]
    send_mail(subject, message, email_from, recipient_list)
    return True


def access_permissions(roles):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = args[1].user
            groups = set(user.groups.values_list("name", flat=True).all())
            if groups.intersection(roles):
                response = func(*args, **kwargs)
                return response
            else:
                raise PermissionDenied
        return wrapper

    return inner


def truncate(number, digits=0) -> float:
    """
    Fn to truncate float values up to req decimal places
    :param number:
    :param digits:
    :return:
    """
    try:
        if digits == 0:
            return round(number, digits)
        number = float(number)
        before_deci, after_deci = str(number).split('.')
        return float(before_deci + "." + after_deci[0:digits])
    except:
        return number


def round_off(value, digits=0):
    try:
        if digits == 0:
            return int(round(value, digits))
        return round(value, digits)
    except Exception:
        return value