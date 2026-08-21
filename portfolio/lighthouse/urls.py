from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('books/', views.search, name='search'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/search-isbn/', views.search_isbn, name='search_isbn'),
    path('books/<int:book_id>', views.book_details, name='book_details'),
    path('books/<int:book_id>/edit/', views.book_update, name='book_update'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('books/return/', views.return_book, name='return_book'),
    path('categories/create/', views.create_category, name='create_category'),
]
