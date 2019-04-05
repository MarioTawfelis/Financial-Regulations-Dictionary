from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .forms import DocumentForm
from .scraper import find_regulator
from .models import Document


def home(request):
    return render(request, 'documents/home.html')


@login_required
def new_document(request):
    if request.GET.get('url', ''):
        url = request.GET.get('url', '')
        form = DocumentForm()

        return render(request, 'documents/scraper_form.html', {'form': form,
                                                               'url': url})
    elif request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.content = find_regulator(document.url)
            document.user_id = request.user.id
            document.save()
            form.save_m2m()
            return redirect('documents:downloads')
    else:
        form = DocumentForm()

    return render(request, 'documents/scraper_form.html', {'form': form})


@login_required
def downloads(request):
    user = request.user
    try:
        documents = Document.objects.filter(user_id=user.id)
    except Document.DoesNotExist:
        documents = None

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


@login_required
def search(request):
    user = request.user

    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        f = request.GET['f']
        print(f)

        try:
            if f == "name":
                documents = Document.objects.filter(user_id=user.id).filter(name__contains=q)
            elif f == "tags":
                documents = Document.objects.filter(user_id=user.id).filter(tags__name__in=q).distinct()
            elif f == "content":
                documents = Document.objects.filter(user_id=user.id).filter(content__contains=q)
            else:
                documents = Document.objects.filter(user_id=user.id).filter(
                    Q(name__contains=q) | Q(tags__name__in=q) | Q(content__contains=q)).distinct()

        except Document.DoesNotExist:
            documents = None

        return render(request, 'documents/downloads_portal.html', {'documents': documents})

    else:
        error = True

        documents = Document.objects.filter(user_id=user.id)

    return render(request, 'documents/downloads_portal.html', {'documents': documents, 'error': error})
