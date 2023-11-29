from django.urls import path

from main import views

urlpatterns = [
    path("register_ticket/", views.RegisterTicketAPIView.as_view()),
    path("verify_otp/", views.VerifyTicketOTPAPIView.as_view()),
    path("get_ticket_type/", views.GetTicketAPIView.as_view()),
]