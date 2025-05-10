from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Document(models.Model):
    ACCESS_CHOICES = [
        ('blocked', 'Bloquear todo acesso'),
        ('view', 'Apenas visualizar'),
        ('view_download', 'Visualizar e baixar'),
        ('full', 'Visualizar, baixar e imprimir'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_CHOICES,
        default='view'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def is_view_only(self):
        return self.access_level == 'view'
