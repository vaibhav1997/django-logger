from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class logger(models.Model):
    log = models.CharField(max_length = 255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ('-log',)

    def __str__(self):
        return self.log
