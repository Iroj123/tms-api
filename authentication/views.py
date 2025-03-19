from typing import Generic

from django.contrib.auth import authenticate
from knox.models import AuthToken
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserSerializer


class RegisterView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        """
        Handle user registration and Knox authentication token creation.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Create a Knox token for the new user
            token = AuthToken.objects.create(user=user)

            return Response({
                "message": "User created successfully",
                "token": token[1],  # The second element is the token string
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        token = AuthToken.objects.create(user)[1]  # Generate Knox token

        return Response({
            'user': {
                'email': user.email,
                'first_name':user.first_name,
                'last_name': user.last_name,
            },
            'token': token,
        }, status=status.HTTP_200_OK)
