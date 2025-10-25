# tasks/urls.py

from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserViewSet

router = DefaultRouter()

# Register the Task ViewSet
router.register(r'tasks', TaskViewSet, basename='task')

# Register the User ViewSet (mainly for registration/creation)
router.register(r'users', UserViewSet, basename='user')

# The router automatically generates the CRUD URLs for us (e.g., /tasks/, /tasks/1/, /tasks/1/complete/)

urlpatterns = router.urls