# authentication/serializers.py
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers

from TaskManagementSystem import settings
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

from rest_framework import serializers
from authentication.models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate that the user exists and the password is correct.
        """
        email = data.get("email")
        password = data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        return data

def send_verification_email(user):
    try:
        send_mail(
            subject="Registration Confirmation",
            message=f"Your verification code is {user.verification_code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
            )
    except Exception as e:
            print(f"Error sending email: {e}")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        # Create the user instance
        user = CustomUser.objects.create_user(**validated_data)

        # Set the default values for verification
        user.is_verified = False  # Set the user as unverified by default
        user.verification_code = get_random_string(length=6, allowed_chars="0123456789")  # Generate OTP
        user.save()  # Save the user to the database

        # Send verification email
        send_verification_email(user)

            # Return the created user instance
        return user



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)  # Assuming OTP is a 6-digit number

    def validate(self, data):
        email = data["email"]
        otp = data["verification_code"]
        # Check if the OTP matches the one stored in the database
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if user.verification_code != otp:
            raise serializers.ValidationError("Invalid OTP.")

        # OTP is valid, you can either mark the user as verified or allow further actions
        user.is_verified = True
        user.save()

        return data



