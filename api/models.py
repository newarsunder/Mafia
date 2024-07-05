from typing import Any
from django.db import models
import random, string, uuid
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
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=20, unique=False)
    password = models.CharField(max_length=100, default='123')
    color = models.CharField(max_length=20)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    host = models.BooleanField(default=False)
    joined_at = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'unique_code'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.color