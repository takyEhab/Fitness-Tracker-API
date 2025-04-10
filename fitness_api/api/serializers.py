from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        if not data.get('activity_type'):
            raise serializers.ValidationError("Activity type is required.")
        if not data.get('duration'):
            raise serializers.ValidationError("Duration is required.")
        if not data.get('date'):
            raise serializers.ValidationError("Date is required.")
        return data
