import time
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .repository import AuthRepository, LinkInviteRepository
from .serializer import AuthSerializer, CodeSerializer, InviteSerializer, UserSerializer, ProfileSerializer, \
    AllNumberInvited


class AuthNumber(APIView):

    @swagger_auto_schema(request_body=AuthSerializer, operation_description="Ввод номера")
    def post(self, request):
        body = AuthSerializer(data=request.data)
        if body.is_valid():
            code = body.generate_code()
            time.sleep(1.2)
            return Response({"code": code}, status=status.HTTP_200_OK)

        return Response(body.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthCode(APIView):

    @swagger_auto_schema(request_body=CodeSerializer, operation_description="Ввод кода для авторизации или регистрации")
    def post(self, request):
        body = CodeSerializer(data=request.data)
        if body.is_valid():
            code = body.validated_data['code']
            try:
                token = AuthRepository.create_user(code)
                return Response({"access_token": token}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(body.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteCode(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER,  description="Bearer token", type=openapi.TYPE_STRING,
                          format="Bearer", )
    ], request_body=InviteSerializer, operation_description="Ввод инвайт кода юзера", )
    def post(self, request):
        user = request.user.pk
        body = InviteSerializer(data=request.data)

        if body.is_valid():
            code = body.validated_data['invite_code']
            result = LinkInviteRepository.link_user_code(code, user)
            if isinstance(result, dict):
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                serialized_user = UserSerializer(result).data
                return Response(serialized_user, status=status.HTTP_200_OK)

        return Response(body.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING,
                          format="Bearer")
    ],  operation_description="Получить данные юзера")
    def get(self, request):
        user_id = request.user.pk
        user = AuthRepository.view_account(user_id)
        serialized_user = ProfileSerializer(user).data
        return Response(serialized_user, status=status.HTTP_200_OK)


class ViewAllInviteUser(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING,
                          format="Bearer")
    ], operation_description="Получить номера всех введенных номеров инвайт кода")
    def get(self, request):
        user_id = request.user.pk
        all_user_invited = LinkInviteRepository.all_user_invited(user_id)
        data = {"numbers": all_user_invited}

        serializer = AllNumberInvited(data=data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
