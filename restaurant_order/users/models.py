from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Клиент'),
        ('waiter', 'Официант'),
        ('chef', 'Повар'),
        ('manager', 'Менеджер'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone = models.CharField(max_length=20, blank=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="resto_user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="resto_user_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

