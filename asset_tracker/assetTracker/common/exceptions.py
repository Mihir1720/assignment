from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.views import exception_handler
from django.shortcuts import redirect
from django.urls import reverse

def custom_exception_handler(exc, context):
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return redirect(reverse("index-page"))
    return exception_handler(exc, context)
