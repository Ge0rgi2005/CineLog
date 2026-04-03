from django import forms
from .models import Watchlist, WatchlistEntry


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ('list_title', 'list_description', 'is_public')
        widgets = {
            'list_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of your watchlist goes here',
            }),
            'list_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional watchlist description goes here',
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'list_title': 'Watchlist Name',
            'list_description': 'Description',
            'is_public': 'Make this watchlist public',
        }
        help_texts = {
            'is_public': 'Public watchlists can be viewed by all users.',
        }

def clean_list_title(self):
    title = self.cleaned_data.get('list_title')
    if not title:
        return title
    if len(title.strip()) < 3:
        raise forms.ValidationError("Watchlist name must be at least 3 characters long.")
    return title.strip()


class WatchlistEntryForm(forms.ModelForm):
    class Meta:
        model = WatchlistEntry
        fields = ('movie', 'notes', 'is_watched', 'watchlist')
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Why do you want to watch this? (optional)',
            }),
            'is_watched': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'movie': forms.Select(attrs={
                'class': 'form-select',
            }),
            'watchlist': forms.HiddenInput(),
        }
        labels = {
            'movie': 'Select Movie',
            'notes': 'Personal Notes',
            'is_watched': 'Already watched',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['watchlist'].disabled = True