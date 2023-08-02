from django.urls import path
from authentication.views import LoginHandler, LogoutHandler, index_page
urlpatterns = [
    path("", index_page, name="index-page"),
    path("login", LoginHandler.as_view(), name="login"),
    path("logout", LogoutHandler.as_view(), name="logout")
]