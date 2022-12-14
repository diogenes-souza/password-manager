from django.db import models
from django.contrib.auth.models import User

class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    siteTitle = models.CharField(max_length=200, null=True, blank=True)

    websiteLink = models.TextField(null=True, blank=True)

    websiteUser = models.CharField(max_length=20, null=True, blank=True)

    websiteEmail = models.CharField(max_length=60, null=True, blank=True)

    websitePassword = models.CharField(max_length=12, null=True, blank=True)

    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.siteTitle

    class Meta:
        ordering = ['createDate']