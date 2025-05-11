from django.contrib import admin
from .models import Document, Fatura

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'access_level')
    list_filter = ('access_level', 'uploaded_at')
    search_fields = ('title', 'description')

@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'valor_total', 'pago')
    actions = ['gerar_pdf']

    def gerar_pdf(self, request, queryset):
        for fatura in queryset:
            # Chama a view via URL reversa
            from django.urls import reverse
            from django.shortcuts import redirect
            return redirect(reverse('gerar_fatura', args=[fatura.id]))
