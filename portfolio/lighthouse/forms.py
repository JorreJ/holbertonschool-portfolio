from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'update-info', 'id': 'title-input'}),
            'author': forms.TextInput(attrs={'class': 'update-info', 'id': 'author-input'}),
            'ISBN': forms.TextInput(attrs={'class': 'update-info', 'id': 'isbn-input', 'required': True, 'minlength': '10', 'maxlength': '13'}),
            'published': forms.NumberInput(attrs={'class': 'update-info', 'id': 'published-input'}),
            'edition': forms.TextInput(attrs={'class': 'update-info', 'id': 'edition-input'}),
            'cover': forms.URLInput(attrs={'class': 'update-info', 'id': 'cover-input'}),
            'category': forms.SelectMultiple(attrs={'class': 'update-info', 'id': 'category-input'}),
            'location': forms.TextInput(attrs={'class': 'update-info', 'id': 'location-input'}),
            'status': forms.TextInput(attrs={'class': 'update-info', 'id': 'status-input'}),
            'cote': forms.TextInput(attrs={'class': 'update-info', 'id': 'cote-input'}),
            'collection': forms.TextInput(attrs={'class': 'update-info', 'id': 'collection-input'}),
            'read_level': forms.TextInput(attrs={'class': 'update-info', 'id': 'read_level-input'}),
            'summary': forms.TextInput(attrs={'class': 'update-info', 'id': 'summary-input'}),
            'language': forms.TextInput(attrs={'class': 'update-info', 'id': 'language-input'}),
            'copy': forms.NumberInput(attrs={'class': 'update-info', 'id': 'copy-input'}),
            #'genre':
        }
