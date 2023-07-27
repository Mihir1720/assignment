from django.urls import path
from authentication.views import LoginHandler, LogoutHandler
urlpatterns = [
    path("login", LoginHandler.as_view(), name="login"),
    path("logout", LogoutHandler.as_view(), name="logout")
]