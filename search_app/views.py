import os
from glob import glob

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from .models import Search, Document


def set_document(request):
    if request.method == 'POST':
        files = glob(settings.FILES + '/*')
        for file in files:
            name = file.split('\\')[-1]
            with open(file) as f:
                text = f.read()
            document = Document(title=name, text=text)
            document.save()
    return render(request, 'search_app/upload_file.html')


def results(request, search_id):
    search = get_object_or_404(Search, pk=search_id)
    return render(request, 'search_app/results_page.html', {'query': search.text, 'result': search.get_result()})


def index(request):
    if request.method == 'GET':
        return render(request, 'search_app/search_page.html')
    if request.method == 'POST':
        query = request.POST['query']
        search, _ = Search.objects.get_or_create(text=query)
        return redirect('result', search_id=search.id)


def help_page(request):
    return render(request, 'search_app/help.html')
