from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)
        return Response({'error': _('Invalid credentials')}, status=400)