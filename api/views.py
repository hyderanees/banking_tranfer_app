from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction

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
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer
    queryset = Bank.objects.all()


class AccountViewSet(viewsets.ModelViewSet, generics.CreateAPIView, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(is_active=True, owner=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_money_in_account(self, request):
        data = request.data
        account_ = Account.objects.filter(is_active=True, id=data['id'], owner=request.user).last()
        if not account_:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        account_.balance = account_.balance + float(data['balance'])
        account_.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def send_money_from_one_account_to_another(self, request):
        data = request.data
        money = float(data['money'])
        sender_account_id = data['sender_account_id']
        receive_account_id = data['receive_account_id']

        sender_account_ = Account.objects.filter(is_active=True, id=sender_account_id,
                                                 owner=request.user).last()
        receive_account_ = Account.objects.filter(id=receive_account_id).last()

        if not sender_account_:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        if sender_account_.id == receive_account_.id:
            return Response({'error': "Cannot send money to same account"}, status=status.HTTP_400_BAD_REQUEST)

        if sender_account_.balance < money:
            return Response({'error': "You don't have enough money"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            receive_account_.balance = receive_account_.balance + money
            receive_account_.save()

            sender_account_.balance = sender_account_.balance - money
            sender_account_.save()
        return Response({}, status=status.HTTP_200_OK)
