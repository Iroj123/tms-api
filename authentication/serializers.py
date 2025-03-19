# authentication/serializers.py
from rest_framework import serializers

from authentication.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'repeat_password']
        extra_kwargs = {
            'password': {'required': True},
            'repeat_password': {'required': True},
        }

    def validate(self, data):
        """
        Check that the password and repeat_password match.
        """
        password = data.get('password')
        repeat_password = data.get('repeat_password')

        if password != repeat_password:
            raise serializers.ValidationError({"repeat_password": "Passwords must match."})

        return data

    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        validated_data.pop('repeat_password', None)  # Remove repeat_password from validated data
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


