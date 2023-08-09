# Authentication views.
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from common.messages import get_message
from authentication.models import CustomUser
from django.shortcuts import render, redirect
from assets.models import AssetTypes, Assets
from django.urls import reverse

def index_page(request):
    if request.user.is_authenticated:
        return render(
            request, 
            "index.html", 
            {
                "user": request.user.email, 
                "assetTypeCount": AssetTypes.get_count(), 
                "assetCount": Assets.get_count()
            }
        )
    else:
        return render(request, "authentication/login.html")

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

    def get(self, request):
        return self.post(request)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        remember_me = request.data.get("rememberMe", "") == "on"
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            CustomUser.update(email=email, updated_values={"remember_user": remember_me})
            return redirect(reverse("index-page"))
        else:
            return render(
                request, 
                "authentication/login.html",
                {
                    "success": False, 
                    "error": True if email is not None else False, 
                    "message": get_message("LOGIN_FAILED"), 
                    "user": email
                }
            )

class LogoutHandler(APIView):
    """
    Logout API
    Allowed Methods: 
        GET
    Args:
        Request object
    Returns:
        Response object.
        sample response:
            {"success": True/False, "message": "<some message>"}
    """

    permission_classes = []

    def get(self, request):
        logout(request)
        return redirect(reverse("login"))
    
class EmailPasswordAuthenticationBackend(ModelBackend):
    """
    Overrided custom authentication method.
    We need to implement it, because by default django"s authentication can only be done 
    on username field, where here we have a requirement to authenticate through email 
    and password.
    """
    def validate_credentials(self, user, password):
        if user.check_password(password) and user.is_system_admin is True:
            return user
        return None
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        custom_auth_model = get_user_model()
        try:
            if email is None:
                email = kwargs.get("username")
            user = custom_auth_model.objects.get(email=email)
        except custom_auth_model.DoesNotExist as exc:
            print("Exception occured in "
                  "EmailAndPasswordAuthenticationBackend.authenticate as", str(exc))
            return None
        else:
            if user.remember_user is True:
                if password is not None:
                    return self.validate_credentials(user=user, password=password)
                else:
                    return user
            else:
                return self.validate_credentials(user=user, password=password)
    
    def get_user(self, user_id):
        custom_auth_model = get_user_model()
        try:
            return custom_auth_model.objects.get(pk=user_id)
        except custom_auth_model.DoesNotExist:
            return None
