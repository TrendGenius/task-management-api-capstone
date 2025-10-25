# core/urls.py

from django.contrib import admin
from django.urls import path, include
from tasks import urls as task_urls # Import the urls from the tasks app

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. API Endpoints for Tasks and Users
    path('api/', include(task_urls)), 
    
    # 2. Authentication URLs (for login/token management)
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]