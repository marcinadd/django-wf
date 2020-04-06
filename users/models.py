from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse

from django_wf.settings import ALLOWED_DOMAIN


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email.split("@")[0]
        return user

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.account.user
        if user.email.split("@")[1] != ALLOWED_DOMAIN:
            raise ImmediateHttpResponse(HttpResponseRedirect(reverse("users:login") + "?err_domain=true"))
