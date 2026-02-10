from django.db import models


class Message(models.Model):
    """Simple model to demonstrate database connection"""
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message {self.id}: {self.content[:50]}"
