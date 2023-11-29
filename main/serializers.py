from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers

from main.models import TicketType
User = get_user_model()

class TicketSerializer(serializers.Serializer):
    ticket_id = serializers.CharField(required=True, allow_null=False)
    amount = serializers.FloatField(required=True, allow_null=False)
    ticket_count = serializers.IntegerField(required=True, allow_null=False)
    def validate(self, attrs):
        ticket_id = attrs.get("ticket_id")
        ticket_ins = TicketType.objects.filter(id=ticket_id, is_active=True).first()
        if ticket_ins is None:
            raise serializers.ValidationError(
                {"error_code": "24", "ticket": f"{ticket_id} does not exist."}
            )
        else:
            if ticket_ins.ticket_amount != attrs.get("amount"):
                raise serializers.ValidationError(
                    {"error_code": "24", "ticket": f"invalid amount for {ticket_ins.ticket_name}."}
                )
        return attrs

class RegisterTicketSerializer(serializers.Serializer):
    data = serializers.ListSerializer(child=TicketSerializer())
    phone_number = serializers.CharField(required=True, allow_null=False)
    email = serializers.EmailField(required=True, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False)
    last_name = serializers.CharField(required=True, allow_null=False)
    country = serializers.CharField(required=True, allow_null=False)
    consent = serializers.BooleanField(required=True, allow_null=False)
    
    def validate(self, attrs):
        if len(attrs["data"]) < 1:
            raise serializers.ValidationError(
                {"error_code": "24", "data": "data cannot be empty"}
            )
        else:
            seen = set()
            for item in attrs.get("data"):
                ticket_id = item.get("ticket_id")
                if ticket_id in seen:
                    raise serializers.ValidationError(
                    {"error_code": "24", "data": f"duplicate {ticket_id} found"}
                )
                seen.add(ticket_id)
        if attrs["consent"] is False:
            raise serializers.ValidationError(
                {"error_code": "24", "consent": "consent cannot be False"}
            )
        return attrs
    
class VerifyTicketOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True, allow_null=False)
    
    def validate(self, attrs):
        email = self.context.get('email')
        otp_code = attrs.get('otp_code') 
        user_ins = User.objects.filter(email=email, is_active=True).first()
        if user_ins:
            if not user_ins.otp_code:
                raise serializers.ValidationError(
                                {"error_code": "24", "otp_code": "invalid otp_code"}
                )
            else:
                if otp_code != user_ins.otp_code:
                    raise serializers.ValidationError(
                                    {"error_code": "24", "otp_code": "incorrect otp_code"}
                    ) 
            if user_ins.is_verified is False:
                user_ins.is_verified = True
                user_ins.save()
        else:
            raise serializers.ValidationError(
                {"error_code": "24", "user": "user does not exist"}
            )
        return attrs
        
class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = "__all__"
