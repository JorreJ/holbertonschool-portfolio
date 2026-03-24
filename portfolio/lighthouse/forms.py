from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'update-info', 'required': True}),
            'author': forms.TextInput(attrs={'class': 'update-info'}),
            'ISBN': forms.TextInput(attrs={'class': 'update-info', 'required': True, 'minlength': '10', 'maxlength': '13'}),
            'published': forms.NumberInput(attrs={'class': 'update-info'}),
            'edition': forms.TextInput(attrs={'class': 'update-info'}),
            #'category':
            'location': forms.TextInput(attrs={'class': 'update-info'}),
            'status': forms.TextInput(attrs={'class': 'update-info'}),
            'cote': forms.TextInput(attrs={'class': 'update-info'}),
            'collection': forms.TextInput(attrs={'class': 'update-info'}),
            'read_level': forms.TextInput(attrs={'class': 'update-info'}),
            'summary': forms.TextInput(attrs={'class': 'update-info'}),
            'language': forms.TextInput(attrs={'class': 'update-info'}),
            'copy': forms.NumberInput(attrs={'class': 'update-info'}),
            #'genre':
        }