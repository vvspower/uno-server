from rest_framework import serializers
import sys 
sys.path.append("..")
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"