# tasks/serializers.py

from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

# --- User Serializer (For Login/Registration) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Expose only the fields necessary for registration/viewing
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True} 
        }

    def create(self, validated_data):
        # Use Django's built-in method to correctly hash the password
        user = User.objects.create_user(**validated_data)
        return user

# --- Task Serializer (For CRUD operations) ---
class TaskSerializer(serializers.ModelSerializer):
    # 'user' is a read-only field that will display the username, not the ID
    user = serializers.ReadOnlyField(source='user.username') 

    class Meta:
        model = Task
        # Fields exposed in the API
        fields = (
            'id', 'user', 'title', 'description', 
            'due_date', 'priority', 'status', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')