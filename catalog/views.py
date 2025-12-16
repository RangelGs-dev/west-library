import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy

from catalog.models import Book, Author, BookInstance, Genre

from catalog.forms import RenewBookForm

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

class AuthorsListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back'))


class ListOfBooksOnLoanLibrarianVision(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_of_books_on_loan_librarian_vision.html'

    def get_queryset(self):
        return (BookInstance.objects.filter(status__exact='o').order_by('due_back'))


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Se for uma solicitação POST, processa os dados do form
    if request.method == 'POST':
        #Instancia um formulario de RenewBookForm e faz o binding dos dados da req.
        form = RenewBookForm(request.POST)

        # Valida o form
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
        
        # Se qualquer outro método, cria-se um form padrão
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model= Author
    success_url = reverse_lazy('authors')