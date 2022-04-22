from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Bank, Account
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, BankSerializer, AccountSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class BankViewSet(viewsets.ModelViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.all()


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
