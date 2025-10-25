# tasks/models.py

from django.db import models
from django.contrib.auth.models import User # Import the built-in User model

# Define choices for the Task fields
PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

class Task(models.Model):
    # The ForeignKey links this Task to a specific User (the user who created it).
    # on_delete=models.CASCADE means if the User is deleted, their tasks are also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Required Fields from the Capstone brief
    due_date = models.DateField(null=True, blank=True)
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    
    class Meta:
        # Order tasks by due date or creation date by default
        ordering = ['due_date', '-created_at']