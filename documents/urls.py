from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.document_upload, name='document_upload'),
    path('<int:pk>/view/', views.document_view, name='document_view'),  # Corrigido aqui
    # Outras URLs...
]
