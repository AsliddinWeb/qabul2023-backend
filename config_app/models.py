from django.db import models

class EskizBearerToken(models.Model):
    token = models.TextField()

class EskizEmailAndPassword(models.Model):
    email = models.CharField(max_length=255)
    password = models.TextField()

class SmsText(models.Model):
    text = models.TextField()