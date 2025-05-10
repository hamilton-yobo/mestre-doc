from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'access_level')
    list_filter = ('access_level', 'uploaded_at')
    search_fields = ('title', 'description')
