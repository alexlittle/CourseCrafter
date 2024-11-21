from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crafter.urls')),
    path('celery-progress/', include('celery_progress.urls')),
]
