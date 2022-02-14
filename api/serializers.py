from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class OfficialsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Officials
        fields='__all__'

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meeting
        fields='__all__'