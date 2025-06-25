from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'dob', 'gender', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Customer(
            username=validated_data['username'],
            email=validated_data['email'],
            dob=validated_data.get('dob'),
            gender=validated_data.get('gender'),
            phone_number=validated_data.get('phone_number')
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
