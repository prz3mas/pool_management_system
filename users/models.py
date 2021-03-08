from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    RECEPTIONIST = 1
    CLEANER = 2
    CONSERVATOR = 3
    MASSEUR = 4
    SWIMMING_COACH = 5
    MANAGER = 6

    USER_TYPE_CHOICES = (
        (RECEPTIONIST, 'recepcjonistka'),
        (CLEANER, 'sprzątaczka'),
        (CONSERVATOR, 'konserwator'),
        (MASSEUR, 'masażysta'),
        (SWIMMING_COACH, 'instruktor pływania'),
        (MANAGER, 'kierownik')
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=None, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = CustomUserManager()

    @staticmethod
    def get_user(email):
        return CustomUser.objects.get(email=email)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
