from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import MEDIA_URL, STATIC_URL
from core.base.models import Persona

class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, blank=True, null=True)
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')