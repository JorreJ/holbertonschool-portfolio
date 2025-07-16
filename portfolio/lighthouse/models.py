from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

class Genre(models.Model):
    name = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=13)
    published = models.IntegerField(null=True, blank=True)
    edition = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    cote = models.CharField(max_length=10)
    collection = models.CharField(max_length=200)
    read_level = models.CharField(max_length=200)
    summary = models.CharField(max_length=2000)
    language = models.CharField(max_length=200)
    copy = models.IntegerField(null=True, blank=True)
    genre = models.ManyToManyField(Genre)

class Borrowing(models.Model):
    borrower = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def is_returned(self):
        return self.return_date is not None
