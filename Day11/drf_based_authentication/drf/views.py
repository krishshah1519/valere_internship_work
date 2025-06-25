#Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer, LoginSerializer
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# VIEWS
class CustomerApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response({
            "status": True,
            "data": serializer.data,
        })

class LoginApi(APIView):

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                    "status":False,
                    "data": serializer.errors
                })
        user  = authenticate(username = serializer.data["username"],password = serializer.data["password"])
        if user:
            token, _ = Token.objects.get_or_create(user = user)

            return Response({
                'status': True,
                'data': {'token': str(token)}
            })
        return Response({
            "status": False,
            "message": 'Invalid credentials'
        })
