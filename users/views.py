from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse
from stronghold.decorators import public

from users import strings


@public
def login(request):
    context = None
    if SocialAccount.objects.all().count() == 0:
        messages.warning(request, strings.WARNING_SOCIAL_APP_NO_CONFIG)
        context = {"button_disabled": True}
    return render(request, "users/login.html", context)


@public
def logout_from_app(request):
    logout(request)
    messages.info(request, strings.INFO_LOGOUT)
    return redirect(reverse('wyniki:index'))
