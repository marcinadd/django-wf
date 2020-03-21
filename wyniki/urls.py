from django.urls import path

from . import views

app_name = "wyniki"
urlpatterns = [
    path('', views.index, name='index'),

    path("classes/create", views.ClassCreate.as_view(), name="classes_create"),
    path("classes/", views.ClassList.as_view(), name="classes_list"),
    path("classes/delete/<int:pk>", views.ClassDelete.as_view(), name="classes_delete"),
    path("classes/update/<int:pk>", views.ClassUpdate.as_view(), name="classes_update"),

    path("students/create", views.StudentCreate.as_view(), name="students_create"),
    path("students/", views.StudentList.as_view(), name="students_list"),
    path("students/delete/<int:pk>", views.StudentDelete.as_view(), name="students_delete"),
    path("students/update/<int:pk>", views.StudentUpdate.as_view(), name="students_update"),

    path("classes/createWithStudents", views.create_class_with_students, name="classes_create_students"),
]