from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

class Genre(models.Model):
    name = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    ISBN = models.CharField(max_length=13)
    published = models.IntegerField(null=True, blank=True)
    edition = models.CharField(max_length=200, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)
    cote = models.CharField(max_length=10, blank=True)
    collection = models.CharField(max_length=200, blank=True)
    read_level = models.CharField(max_length=200, blank=True)
    summary = models.CharField(max_length=2000, blank=True)
    language = models.CharField(max_length=200, blank=True)
    copy = models.IntegerField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True)

class Borrowing(models.Model):
    borrower = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def is_returned(self):
        return self.return_date is not None
