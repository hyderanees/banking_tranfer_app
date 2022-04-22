from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Bank, Account


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(allow_blank=True, default='')
    IBAN = serializers.CharField(allow_blank=True, default='')
    balance = serializers.IntegerField(default=0)

    class Meta:
        model = Account
        fields = ('id', 'title', 'bank', 'owner', 'IBAN', 'balance')

    def validate(self, attrs):
        user = self.context['request'].user
        if Account.objects.filter(owner=user).count() >= 2:
            raise serializers.ValidationError({"error": "You cannot make more than 5 accounts"})

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            account_ = Account.objects.create(owner=self.context['request'].user, title=validated_data['title'],
                                              bank=validated_data['bank'])
            return account_
