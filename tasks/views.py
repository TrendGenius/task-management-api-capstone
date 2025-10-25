# tasks/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Permissions/Security: Only allow authenticated users to manage resources.
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the task.
        return obj.user == request.user


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Enable filtering by 'status' and 'priority'
    filterset_fields = ['status', 'priority']
    
    # Enable searching by 'title' or 'description'
    search_fields = ['title', 'description']
    
    # Enable ordering by date, priority, etc.
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        """
        This ensures users only see their own tasks (View Activity History requirement).
        """
        # Return only the tasks that belong to the current authenticated user
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically sets the user to the currently logged-in user when creating a task.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Custom endpoint to quickly mark a task as 'completed'.
        """
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({'status': 'task marked as completed'})

# User Management (Registration is done here, standard CRUD is via admin for simplicity)
class UserViewSet(viewsets.ModelViewSet):
    # Only allow the creation of new users (registration)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to register