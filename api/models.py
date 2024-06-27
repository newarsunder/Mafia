from typing import Any
from django.db import models
import random, string
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=6, unique=True, blank=True)
    max_capacity = models.IntegerField(default=10)
    public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase, k=6))
            if not Room.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, default='123')
    color = models.CharField(max_length=20)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    host = models.BooleanField(default=False)
    joined_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.username