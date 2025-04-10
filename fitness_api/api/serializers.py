from rest_framework import serializers
from .models import Activity
from django.contrib.auth.models import User

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        if not data.get('activity_type'):
            raise serializers.ValidationError("Activity type is required.")
        if not data.get('duration'):
            raise serializers.ValidationError("Duration is required in minutes.")
        if not data.get('date'):
            raise serializers.ValidationError("Date is required.")
        return data



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    # def validate(self, data):
    #     if not data.get('username'):
    #         raise serializers.ValidationError("Username is required.")
    #     if not data.get('email'):
    #         raise serializers.ValidationError("Email is required.")
    #     if not data.get('password'):
    #         raise serializers.ValidationError("Password is required.")
    #     return data
