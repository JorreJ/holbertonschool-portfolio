import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Book, Borrowing
from .forms import BookForm
from django.utils import timezone
from .services import BookLookup

# Create your views here.
def accueil(request):
    return render(request, 'home_page.html')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            messages.success(request, f'"{new_book.title}" a bien été enregistré.')
            return redirect('add_book')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def search_isbn(request):
    isbn = request.GET.get("isbn")
    if not isbn:
        return JsonResponse({})
    data = BookLookup.search(isbn)
    if data is None:
        return JsonResponse({})
    return JsonResponse(data)

def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrowing = Borrowing.objects.filter(book=book, return_date__isnull=True).first()
    return render(request, 'book_details.html', {'book': book, 'borrowing': borrowing})

def search(request):
    books = Book.objects.all()

    search_fields = {
        'title': 'title__icontains',
        'author': 'author__icontains',
        'published': 'published',
        'ISBN': 'ISBN__icontains',
        'location': 'location__icontains',
        'status': 'status__icontains',
        'cote': 'cote__icontains',
        'collection': 'collection__icontains',
        'read_level': 'read_level__icontains',
        'summary': 'summary__icontains',
        'language': 'language__icontains',
        'copy': 'copy',
    }

    filters = {}
    for field, lookup in search_fields.items():
        value = request.GET.get(field)
        if value:
            filters[lookup] = value
    
    books = books.filter(**filters)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'book_list.html', {'books': books})
    
    return render(request, 'search.html', {'books': books})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('search')

def return_book(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        borrowing = Borrowing.objects.filter(
            book__ISBN=identifier,
            return_date__isnull=True
        ).first()

        if borrowing:
            borrowing.return_date = timezone.now()
            borrowing.save()

            book = borrowing.book
            book.status = 'Disponible'
            book.save()
    return render(request, 'return_book.html')

def borrow_book(request, book_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        borrower_name = data.get('borrower')
        book = get_object_or_404(Book, pk=book_id)

        if book.status != "Disponible":
            return JsonResponse({'message': 'Ce livre est indisponible pour le moment'}, status=400)

        if borrower_name:
            Borrowing.objects.create(
                borrower=borrower_name,
                book=book,
                borrow_date=timezone.now()
            )
            book.status = "Emprunté"
            book.save()
            
            return JsonResponse({'message': f'Livre emprunté par {borrower_name}.'})
    return JsonResponse({'message': 'Erreur lors de l\'emprunt.'}, status=400)

def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_details', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, "book_update.html", {"form": form, "book": book})
