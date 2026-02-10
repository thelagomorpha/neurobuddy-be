from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at']
    search_fields = ['content']
    list_filter = ['created_at']
