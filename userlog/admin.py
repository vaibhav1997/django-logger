from django.contrib import admin
from .models import *

# Register your models here.
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'log')
    readonly_fields = ['log', 'user']

admin.site.register(logger, LoggerAdmin)
