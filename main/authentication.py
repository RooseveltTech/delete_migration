from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication



class CustomTokenAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'