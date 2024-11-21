from django.urls import path, include

from crafter import views

app_name = 'crafter'
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("course/setup", views.SetupCourseView.as_view(), name="setup"),
    path("course/<int:id>/generate", views.GenerateCourseView.as_view(), name="generate"),
]