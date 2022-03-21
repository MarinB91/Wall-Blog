from rest_framework import serializers
from home.models import Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    username = UserSerializer(many=False)

    class Meta:
        model = Message
        fields = '__all__'
