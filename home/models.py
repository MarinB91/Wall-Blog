from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30, blank=False)
    text = models.TextField(max_length=500, blank=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CastedVotes(models.Model):
    username = models.ManyToManyField(User)
    message = models.ManyToManyField(Message)
    vote = models.CharField(max_length=50, blank=False)
    identification = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.identification
