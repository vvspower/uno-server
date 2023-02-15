from rest_framework import serializers
from .models import User
# from .models import UserProfile


class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

# class UserProfileSerialzier(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"
#         extra_kwargs = {'password': {'write_only': True}}
