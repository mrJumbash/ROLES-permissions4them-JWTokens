from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, generics
from .serializers import *
from .emails import send_otp_via_email
from django.contrib.auth import authenticate


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data.get("email")
                password = serializer.data.get("password")
                user = authenticate(email=email, password=password)

                if user is None:
                    return Response(
                        {
                            "status": 400,
                            "message": "invalid password or email",
                            "data": {},
                        }
                    )

                if user.is_verified is False:
                    return Response(
                        {"status": 400, "message": "your acc not verified", "data": {}}
                    )

                refresh = RefreshToken.for_user(user)

                return Response(
                    data={
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )

            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data["email"])
                return Response(
                    {
                        "status": 200,
                        "message": "registered check email",
                        "data": serializer.data,
                    }
                )
            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)


class VerifyAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyUserSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data.get("email")
                otp = serializer.data.get("otp")
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong",
                            "data": "invalid email",
                        }
                    )

                if not user[0].otp == otp:
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong",
                            "data": "invalid otp",
                        }
                    )
                user = user.first()
                user.is_verified = True
                user.save()

                return Response({"status": 200, "message": "user verified", "data": {}})
        except Exception as e:
            print(e)
