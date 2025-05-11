from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Document, Fatura
from .forms import DocumentForm
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import qrcode
import qrcode.image.svg
import base64
import uuid


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


def verificar_fatura(request, codigo):
    fatura = get_object_or_404(Fatura, codigo_verificacao=codigo)
    return render(request, 'faturas/verificacao.html', {'fatura': fatura})

@login_required
@permission_required('app_label.pode_emitir_faturas', raise_exception=True)
def gerar_fatura_pdf(request, fatura_id):
    fatura = Fatura.objects.get(id=fatura_id)
    
    # Gera QR Code único
    verificacao_url = request.build_absolute_uri(fatura.get_absolute_url())
    qr = qrcode.make(verificacao_url, image_factory=qrcode.image.svg.SvgImage)
    buffer = BytesIO()
    qr.save(buffer)
    qrcode_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Dados de exemplo (substitua pelos seus modelos reais)
    itens = fatura.itens
    
    context = {
        'fatura': fatura,
        'itens': itens,
        'qrcode': qrcode_base64
    }
    
    template = get_template('faturas/template.html')
    html = template.render(context)
    
    # Cria PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        # Salva no Cloudinary
        from cloudinary import uploader
        response = uploader.upload(
            result.getvalue(),
            folder="faturas",
            resource_type="raw",
            public_id=f"fatura_{fatura.numero}",
            format="pdf"
        )
        
        # Atualiza o modelo
        fatura.pdf = response['secure_url']
        fatura.codigo_verificacao = str(uuid.uuid4()).replace('-', '')[:16]
        fatura.save()
        
        # Retorna o PDF para download
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="fatura_{fatura.numero}.pdf"'
        return response
    
    return HttpResponse("Erro ao gerar PDF", status=500)


