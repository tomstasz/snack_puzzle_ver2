from django.core.exceptions import ValidationError
from .models import User


def validate_login(value):
    logins = User.objects.all()
    for i in logins:
        if i.username == value:
            raise ValidationError('taki e-mail jest już zajęty')
