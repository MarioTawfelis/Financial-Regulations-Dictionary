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
    # Check if user is trying to scrape via News Feed
    # If yes, pass URL to Scraper form
    if request.GET.get('url', ''):
        url = request.GET.get('url', '')
        form = DocumentForm()

        return render(request, 'documents/scraper_form.html', {'form': form,
                                                               'url': url})
    elif request.method == 'POST':  # True if user is submitting the form
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            if find_regulator(document.url) is not None:  # Check that user entered a valid URL
                document.content = find_regulator(
                    document.url)  # Fetch script and return content of regulatory update as string
                document.user_id = request.user.id  # Add current user ID to allow for personalization of Downloads Portal
                document.save()
                form.save_m2m()  # Save meta-tags
                return redirect('documents:downloads')
            else:  # User entered invalid or unsupported URL
                error = True

    else:  # Just load form
        form = DocumentForm()

    return render(request, 'documents/scraper_form.html', {'form': form, 'error': error})


@login_required
def downloads(request):
    user = request.user
    try:
        documents = Document.objects.filter(user_id=user.id)  # Retrieve all documents that a user has captured
    except Document.DoesNotExist:
        documents = None

    return render(request, 'documents/downloads_portal.html', {'documents': documents})


""" Title: Having Django serve downloadable files
Author: Stanislaus Madueke
Date:  Jul 21 '09
Availability: https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files """


@login_required
def download_document(request, pk):
    document = Document.objects.get(pk=pk)
    # Prepare document to be served as a downloadable HTML file
    filename = document.name
    content = document.content
    response = HttpResponse(content, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="%s.html"' % filename
    return response


@login_required
def delete_document(request, pk):
    Document.objects.filter(id=pk).delete()  # Delete document with a specific ID
    return redirect('documents:downloads')


@login_required
def search(request):
    user = request.user

    if 'q' in request.GET and request.GET['q']:  # Check if user input a search term
        q = request.GET['q']  # Get search term
        f = request.GET['f']  # Get search criteria

        # Find search criterion and retrieve relevant data
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
