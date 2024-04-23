from django.contrib import admin

from .models import EskizBearerToken, EskizEmailAndPassword, SmsText

admin.site.register([EskizBearerToken, EskizEmailAndPassword, SmsText])