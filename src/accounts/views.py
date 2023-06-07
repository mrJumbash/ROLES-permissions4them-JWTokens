from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    ConfirmCodeSerializer,
)
from accounts.models import ConfirmCode, User, TenantCode
from django.contrib.auth import authenticate
from common.utils import activate_code
from accounts.services import UserService

"""Tenant Setting"""


class TenantSetAPI(APIView):
    def get(self, request):
        if not request.user.is_anonymous:
            if request.user.role not in (1, 3):
                code = TenantCode.objects.create(
                    user_id=request.user.id, code=activate_code
                )
                return Response(
                    status=status.HTTP_200_OK,
                    data={"user_id": code.user_id, "code": code.code},
                )
        else:
            return Response(data={"message": "Please authorize!"})

    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if TenantCode.objects.filter(code=request.data["code"]):
            User.objects.update(role=2)
            return Response(
                status=status.HTTP_202_ACCEPTED,
                data={"success": "confirmed", "role": request.user.role},
            )

        return Response(
            status=status.HTTP_406_NOT_ACCEPTABLE,
            data={"error": "something went wrong"},
        )


"""ADMIN REGISTRATION"""


class RegistrationAdminAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        email = serializer.validated_data.get("email")
        user = User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )
        return Response(
            status=status.HTTP_201_CREATED, data={"user_id": user.id, "role": user.role}
        )


"""BUYER REGISTRATION"""


class RegistrationBuyerAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        email = serializer.validated_data.get("email")
        user = User.objects.create_user(
            username=username, password=password, role=3, email=email
        )
        code = ConfirmCode.objects.create(user_id=user.id, code=activate_code)
        return Response(
            status=status.HTTP_201_CREATED,
            data={"user_id": user.id, "role": user.role, "code": code.code},
        )


"""Sending Confirmation Code"""


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if ConfirmCode.objects.filter(code=request.data["code"]):
                User.objects.update(is_verified=True)
                return Response(
                    status=status.HTTP_202_ACCEPTED, data={"success": "confirmed"}
                )

            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"error": "wrong id or code!"},
            )

        except ValueError:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"error": "write code number!"},
            )


"""Login to get JWT-tokens"""


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if user:
            return UserService.tokens(user=user)

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={"error": "Username or password wrong!"},
        )
