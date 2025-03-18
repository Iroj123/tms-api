# authentication/serializers/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # This will automatically use CustomUser
        fields = ['username', 'email', 'phone_number', 'password']  # Include any extra fields you want

    def create(self, validated_data):
        # Hash the password before saving the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
