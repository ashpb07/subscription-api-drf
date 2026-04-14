from rest_framework import serializers
from .models import Log


class LogSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", default=None)

    class Meta:
        model = Log
        fields = ["id", "user", "action", "status", "timestamp"]

