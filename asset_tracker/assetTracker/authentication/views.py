# Authentication views.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from common.messages import get_message
from rest_framework import status
from authentication.models import CustomUser

class LoginHandler(APIView):
    """
    Login API
    Allowed Methods: 
        POST
    Args:
        Request object
    Returns:
        Response based on authentication.
        sample response:
            {"success": True/False, "message": "<some message>"}
    """

    permission_classes = []

    def post(self, request):
        email = request.GET.get("email")
        password = request.GET.get("password")
        remember_me = request.GET.get("rememberMe", False)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            CustomUser.update(email=email, updated_values={"remember_user": remember_me})
            return Response(
                {
                    "success": True,
                    "message": get_message("LOGIN_SUCCESSFUL")
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "success": False, 
                    "message": get_message("LOGIN_FAILED")
                }, 
                status=status.HTTP_200_OK
            )

class LogoutHandler(APIView):
    """
    Logout API
    Allowed Methods: 
        POST
    Args:
        Request object
    Returns:
        Response object.
        sample response:
            {"success": True/False, "message": "<some message>"}
    """

    permission_classes = []

    def post(self, request):
        logout(request)
        return Response(
            {
                "success": True, 
                "message": get_message("LOGOUT_SUCCESSFUL")
            }, 
            status=status.HTTP_200_OK
        )
    
class EmailPasswordAuthenticationBackend(ModelBackend):
    """
    Overrided custom authentication method.
    We need to implement it, because by default django's authentication can only be done 
    on username field, where here we have a requirement to authenticate through email 
    and password.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        custom_auth_model = get_user_model()
        try:
            if email is None:
                email = kwargs.get("username")
            user = custom_auth_model.objects.get(email=email)
        except custom_auth_model.DoesNotExist as exc:
            print("Exception occured in "
                  "EmailAndPasswordAuthenticationBackend.authenticate as ", str(exc))
            return None
        else:
            if user.remember_user is True:
                return user
            elif user.check_password(password) and user.is_system_admin is True:
                return user
    
    def get_user(self, user_id):
        custom_auth_model = get_user_model()
        try:
            return custom_auth_model.objects.get(pk=user_id)
        except custom_auth_model.DoesNotExist:
            return None
