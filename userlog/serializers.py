from rest_framework import serializers
from .models import *
from rest_framework.response import Response


class LoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = logger
        fields = '__all__'