# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from .models import Document
# from .forms import DocumentForm
# from django.views.decorators.clickjacking import xframe_options_exempt
#
# def document_list(request):
#     documents = Document.objects.all()
#     return render(request, 'documents/document_list.html', {'documents': documents})
#
# @xframe_options_exempt  # Permite embed do PDF
# def document_detail(request, pk):
#     document = get_object_or_404(Document, pk=pk)
#     
#     if document.access_level == 'blocked':
#         return HttpResponseForbidden("Acesso a este documento está bloqueado.")
#     
#     context = {
#         'document': document,
#         'can_view': document.access_level in ['view', 'view_download', 'full'],
#         'can_download': document.access_level in ['view_download', 'full'],
#         'can_print': document.access_level == 'full',
#         'view_only': document.access_level == 'view',  # Novo contexto
#     }
#     
#     return render(request, 'documents/document_detail.html', context)
#
#
#
# # def document_detail(request, pk):
# #     document = get_object_or_404(Document, pk=pk)
# #     
# #     # Verificar permissões
# #     if document.access_level == 'blocked':
# #         return HttpResponseForbidden("Acesso a este documento está bloqueado.")
# #     
# #     context = {
# #         'document': document,
# #         'can_view': document.access_level in ['view', 'view_download', 'full'],
# #         'can_download': document.access_level in ['view_download', 'full'],
# #         'can_print': document.access_level == 'full',
# #     }
# #     
# #     return render(request, 'documents/document_detail.html', context)
#
# @login_required
# def document_upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save(commit=False)
#             document.uploaded_by = request.user
#             document.save()
#             return redirect('document_list')
#     else:
#         form = DocumentForm()
#     return render(request, 'documents/document_upload.html', {'form': form})
#
# @xframe_options_exempt  # Agora devidamente importado
# def document_view(request, pk):
#     document = get_object_or_404(Document, pk=pk)
#     
#     if document.access_level == 'blocked':
#         return HttpResponseForbidden("Acesso bloqueado. Efetue o pagamento para visualizar este documento.")
#     
#     return render(request, 'documents/document_view.html', {
#         'document': document,
#         'is_protected': document.access_level == 'view'
#     })
#
# documents/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Document
from .forms import DocumentForm

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})

@xframe_options_exempt
def document_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if document.access_level == 'blocked':
        return HttpResponseForbidden("Pagamento necessário para acesso.")
    
    return render(request, 'documents/document_view.html', {
        'document': document,
        'is_protected': document.access_level == 'view'
    })

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_upload.html', {'form': form})
