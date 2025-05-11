from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.document_upload, name='document_upload'),
    path('<int:pk>/view/', views.document_view, name='document_view'),  # Corrigido aqui
    path('faturas/gerar/<int:fatura_id>/', views.gerar_fatura_pdf, name='gerar_fatura'),
    path('faturas/verificar/<str:codigo>/', views.verificar_fatura, name='verificar_fatura'),
]
