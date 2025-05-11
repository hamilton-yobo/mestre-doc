from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

class Fatura(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20, unique=True)
    data_emissao = models.DateField(auto_now_add=True)
    vencimento = models.DateField()
    itens = models.JSONField(default=list, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)
    pdf = models.FileField(upload_to='faturas/', null=True, blank=True)
    codigo_verificacao = models.CharField(max_length=32, unique=True)

    def get_absolute_url(self):
        return reverse('verificar_fatura', args=[self.codigo_verificacao])

    def __str__(self):
        return f"Fatura #{self.numero} - {self.cliente.username}"


