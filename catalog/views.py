from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    number_books = Book.objects.all().count()
    number_instances = BookInstance.objects.all().count()

    number_instances_available = BookInstance.objects.filter(status__exact='a').count()

    number_authors = Author.objects.count()

    context = {
        'number_books': number_books,
        'number_instances': number_instances,
        'number_instances_available': number_instances_available,
        'number_authors': number_authors,
    }

    return render(request, 'index.html', context=context)