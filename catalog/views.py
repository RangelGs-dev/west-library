from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    number_books = Book.objects.all().count()
    number_instances = BookInstance.objects.all().count()

    number_instances_available = BookInstance.objects.filter(status__exact='a').count()

    number_authors = Author.objects.count()

    number_visits = request.session.get('number_visits', 0)
    number_visits += 1
    request.session['number_visits'] = number_visits

    context = {
        'number_books': number_books,
        'number_instances': number_instances,
        'number_instances_available': number_instances_available,
        'number_authors': number_authors,
        'number_visits': number_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book