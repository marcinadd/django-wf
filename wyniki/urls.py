from django.urls import path

from . import views

app_name = "wyniki"
urlpatterns = [
    path('', views.index, name='index'),

    path("classes/", views.ClassListView.as_view(), name="classes_list"),
    path("classes/delete/<int:pk>", views.ClassDeleteView.as_view(), name="classes_delete"),
    path("classes/update/<int:pk>", views.ClassUpdateView.as_view(), name="classes_update"),

    path("students/create", views.StudentCreateView.as_view(), name="students_create"),
    path("students/delete/<int:pk>", views.StudentDeleteView.as_view(), name="students_delete"),
    path("students/update/<int:pk>", views.StudentUpdateView.as_view(), name="students_update"),

    path("classes/createWithStudents", views.create_class_with_students, name="classes_create"),
    path("classes/<int:class_id>/results/<int:sport_id>", views.get_results_for_class, name="classes_results"),
    path("classes/<int:pk>/sports", views.get_sports_details_by_class, name="classes_sports"),
    path("classes/<int:pk>/students", views.get_students_by_class, name="classes_students"),
    path("students/<int:student_id>/sports/<int:sport_id>/groups/<int:group_id>", views.ResultCreateView.as_view(),
         name="results_create"),

    path("results/update/<int:pk>", views.ResultUpdateView.as_view(), name="results_update"),
    path("results/delete/<int:pk>", views.ResultDeleteView.as_view(), name="results_delete"),

    path("sports/create", views.SportCreateView.as_view(), name="sports_create"),
    path("sports/list", views.SportListView.as_view(), name="sports_list"),
    path("sports/update/<int:pk>", views.SportUpdate.as_view(), name="sports_update"),
    path("sports/delete/<int:pk>", views.SportDeleteView.as_view(), name="sports_delete"),

    path("user/results", views.get_user_results, name="user_results")
]