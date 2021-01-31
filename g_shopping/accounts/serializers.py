from rest_framework import serializers
from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import  User

class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        max_length=30,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=30,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        help_text="Please enter your personal email address only.",
    )
    confirm_password = serializers.CharField(max_length=50, style={'input_type': 'password',
                                                                   'placeholder': 'Confirm Password*'})

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password and confirm password should match"})
        return data

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user.exists():
            raise serializers.ValidationError({"email": "User with provided email already exists."})
        return value

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def create(self, *args, **kwargs):
        user = User.objects.create(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            password=make_password(self.validated_data['password']),
            is_staff=False,
        )
        return user


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active', 'created_at']


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser
        # ...
        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        users = User.objects.filter(email=attrs['email'])
        if users.exists():
            if not users.first().is_active and users.first().check_password(attrs['password']):
                raise exceptions.AuthenticationFailed({
                    'no_active_account': 'This account is not verified yet. Please verify your account first by'
                                         ' clicking on the verification link sent to your email and then try again.'})
            user = authenticate(**authenticate_kwargs)
            if user is None or not user.is_active:
                raise exceptions.AuthenticationFailed({
                    'no_active_account': 'Please enter a correct email address and password. '
                                         'Note that both fields may be case-sensitive.'})
        else:
            raise exceptions.AuthenticationFailed({
                'no_active_account': 'Please enter a correct email address and password. '
                                     'Note that both fields may be case-sensitive.'})

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if not self.user.is_superuser:
            data['first_name'] = self.user.first_name
            data['last_name'] = self.user.last_name
        data['user_cart'] = self.user.cart.all().count()
        return data