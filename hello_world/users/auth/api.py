# Third Party Stuff
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

# Hello World Stuff
from hello_world.base import response
from hello_world.base.api.mixins import MultipleSerializerMixin
from hello_world.users.services import (
    get_and_authenticate_user,
    get_user_by_email,
    create_user_account,
)

from hello_world.users.auth.serializers import (
    AuthUserSerializer,
    LoginSerializer,
    EmptySerializer,
    PasswordChangeSerializer,
    RegisterSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
)
from hello_world.users.auth.services import send_password_reset_mail_task
from hello_world.users.auth.tokens import get_user_for_password_reset_token


class AuthViewSet(MultipleSerializerMixin, viewsets.GenericViewSet):

    permission_classes = [AllowAny]
    serializer_classes = {
        "login": LoginSerializer,
        "register": RegisterSerializer,
        "logout": EmptySerializer,
        "password_change": PasswordChangeSerializer,
        "password_reset": PasswordResetSerializer,
        "password_reset_confirm": PasswordResetConfirmSerializer,
    }
    response_serializer_class = AuthUserSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = self.response_serializer_class(user).data
        return response.Ok(data)

    @action(methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        response_data = self.response_serializer_class(user).data
        return response.Created(response_data)

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """
        Calls Django logout method; Does not work for UserTokenAuth.
        """
        logout(request)
        return response.Ok({"success": "Successfully logged out."})

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return response.NoContent()

    @action(methods=["POST"], detail=False)
    def password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_by_email(serializer.data["email"])
        if user:
            send_password_reset_mail_task.apply_async([user.id])
        return response.Ok(
            {"message": "Further instructions will be sent to the email if it exists"}
        )

    @action(methods=["POST"], detail=False)
    def password_reset_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_for_password_reset_token(serializer.validated_data["token"])
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return response.NoContent()
