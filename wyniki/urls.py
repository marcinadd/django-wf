from django.urls import path

from . import views

app_name = "wyniki"
urlpatterns = [
    path('', views.index, name='index'),
    path("classes/create", views.ClassCreate.as_view(), name="classes_create"),
    path("classes/", views.ClassList.as_view(), name="classes_list")
]