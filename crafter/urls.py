from django.urls import path, include
from django.contrib.auth.views import LoginView
from crafter import views
from crafter.forms import UserLoginForm

app_name = 'crafter'
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path('login/', LoginView.as_view(
            template_name="crafter/login.html",
            authentication_form=UserLoginForm
            ), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("course/setup", views.SetupCourseView.as_view(), name="setup"),
    path("course/<int:id>/generate", views.GenerateCourseView.as_view(), name="generate"),
    path("course/version/<int:id>/view", views.CourseVersionView.as_view(), name="versionview"),
]