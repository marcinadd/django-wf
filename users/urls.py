from django.urls import path
from django.views.generic import TemplateView

from users import views

app_name = "users"
urlpatterns = [
    path("login", TemplateView.as_view(template_name="users/login.html"), name="login"),
    path("logout", views.wyloguj, name="logout"),
]
