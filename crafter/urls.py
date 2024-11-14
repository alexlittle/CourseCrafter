from django.urls import path

from crafter import views

app_name = 'crafter'
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
]