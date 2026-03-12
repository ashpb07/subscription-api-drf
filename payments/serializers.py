from rest_framework import serializers

class StartUpgradeSerializer(serializers.Serializer):
    plan_name = serializers.CharField()