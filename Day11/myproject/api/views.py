from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from .models import Customer
from django.contrib.auth import login

@api_view(['POST'])
@permission_classes([AllowAny])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Customer created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def log_in(request):
    if request.method == 'Post':
        username = request.get['username']
        password = request.get['password']

        if Customer.objects.filter(username= username ,password = password).exists:
            login(username,password)


