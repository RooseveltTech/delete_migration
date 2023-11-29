from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from main.helpers.func import get_ip_address
from main.models import GameTicket, TicketType

from main.serializers import RegisterTicketSerializer, TicketTypeSerializer, VerifyTicketOTPSerializer
# Create your views here.

User = get_user_model()

class RegisterTicketAPIView(APIView):
    def post(self, request):
        
        serializer = RegisterTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.get("data")
        phone_number = serializer.validated_data.get("phone_number")
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        country = serializer.validated_data.get("country")
        consent = serializer.validated_data.get("consent")
        ip_address = get_ip_address(request)
        ticket_ins = GameTicket.register_ticket(
            data=data, 
            phone_number=phone_number,
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            country=country, 
            consent=consent, 
            ip_address=ip_address
        )
        response = {
                "status_code": "00",
                "message": "successful!"
            }
        return Response(response, status=status.HTTP_200_OK)
    
class VerifyTicketOTPAPIView(APIView):
    def post(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"message": "email missing from parameter"},status=status.HTTP_400_BAD_REQUEST)
        serializer = VerifyTicketOTPSerializer(data=request.data, context={"email":email})
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data.get("otp_code")
        response = {
                "status_code": "00",
                "message": "otp verified!",
                "otp_code": otp_code,
                "email": email
            }
        return Response(response, status=status.HTTP_200_OK)
        
class GetTicketAPIView(APIView):    
    def get(self, request):
        all_ticket = TicketType.objects.filter(is_active=True)
        serializer = TicketTypeSerializer(all_ticket, many=True)
        response = {
                "message": "successful",
                "data": serializer.data
            }
        return Response(response, status=status.HTTP_200_OK)