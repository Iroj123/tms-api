# authentication/views.py
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from knox.models import AuthToken
from authentication.serializers.serializers import UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Save the user
            token = AuthToken.objects.create(user)[1]  # Generate Knox token

            return Response({
                'user': serializer.data,
                'token': token,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        token = AuthToken.objects.create(user)[1]  # Generate Knox token

        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
            },
            'token': token,
        }, status=status.HTTP_200_OK)
