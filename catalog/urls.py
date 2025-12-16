from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.AuthorsListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('borrowed/', views.ListOfBooksOnLoanLibrarianVision.as_view(), name='all-borrowed'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
