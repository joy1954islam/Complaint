from django.db import models
from django.conf import settings
from SuperAdmin.models import Ministry


class Complaint(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ministry_name = models.ForeignKey(Ministry, on_delete=models.CASCADE, verbose_name='Ministry Name')
    location = models.TextField(verbose_name='Location')
    image = models.ImageField(verbose_name='Location Image')
    note = models.TextField(verbose_name='Note')
    is_approved_status = models.BooleanField(default=False)
    is_next_update_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username.username)
