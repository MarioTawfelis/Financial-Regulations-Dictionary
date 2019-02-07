from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DocumentForm
from .scraper import scrapeFCA
from .models import Document


def home(request):
    return render(request, 'documents/home.html')


@login_required
def new_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.content = scrapeFCA(document.url)
            document.save()
            form.save_m2m()
            return redirect('documents:downloads')
    else:
        form = DocumentForm()

    return render(request, 'documents/scraper_form.html', {'form': form})


@login_required
def downloads(request):
    documents = Document.objects.all()
    return render(request, 'documents/downloads_portal.html', {'documents': documents})


@login_required
def download_document(request, pk):
    document = Document.objects.get(pk=pk)
    filename = document.name
    content = document.content
    response = HttpResponse(content, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="%s.html"' % filename
    return response


@login_required
def delete_document(request, pk):
    Document.objects.filter(id=pk).delete()
    return redirect('documents:downloads')
