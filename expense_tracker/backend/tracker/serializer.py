from rest_framework import serializers
from .models import User, Expense


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password", "password2",
            "first_name", "last_name", "dob", "gender", "phone_number"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password2": "Passwords do not match"})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already registered"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "user", "amount", "category", "description", "date"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True}
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero.")
        return value


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password",
            "first_name", "last_name", "dob", "gender", "phone_number"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already registered"})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
