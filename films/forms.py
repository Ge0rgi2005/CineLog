from django import forms
from .models import Movie, CastMember


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = (
            'movie_title',
            'director',
            'year',
            'plot',
            'poster',
            'language',
            'duration',
            'genre',
        )
        widgets = {
            'movie_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Movie title goes here',
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Director name goes here',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Release year goes here',
                'min': 1888,
                'max': 9999,
            }),
            'plot': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your brief plot summary goes here',
            }),
            'language': forms.Select(attrs={
                'class': 'form-select',
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duration (in minutes) goes here',
                'min': 1,
            }),
            'genre': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'movie_title': 'Title',
            'year': 'Release Year',
            'plot': 'Plot Summary',
            'duration': 'Duration (minutes)',
            'genre': 'Genres',
        }
        help_texts = {
            'poster': 'Upload a poster image (JPG or PNG recommended).',
            'genre': 'Select all genres that apply.',
        }

def clean_year(self):
    year = self.cleaned_data.get('year')
    if not year:
        return year
    if year < 1888 or year > 9999:
        raise forms.ValidationError("Please enter a valid release year between 1888 and 9999.")
    return year

def clean_duration(self):
    duration = self.cleaned_data.get('duration')
    if not duration:
        return duration
    if duration < 1:
        raise forms.ValidationError("Duration must be at least 1 minute.")
    return duration

def clean_movie_title(self):
    title = self.cleaned_data.get('movie_title')
    if not title:
        return title
    if len(title.strip()) < 1:
        raise forms.ValidationError("Please enter a valid movie title.")
    return title.strip()


class CastMemberForm(forms.ModelForm):
    class Meta:
        model = CastMember
        fields = ('person_name', 'person_role', 'character_name')
        widgets = {
            'person_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Person's full name goes here",
            }),
            'person_role': forms.Select(attrs={
                'class': 'form-select',
            }),
            'character_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Character name (if applicable) goes here',
            }),
        }
        labels = {
            'person_name': 'Name',
            'person_role': 'Role',
            'character_name': 'Character Name',
        }
        help_texts = {
            'character_name': 'Leave blank for non-acting roles like Director or Composer.',
        }

def clean_person_name(self):
    name = self.cleaned_data.get('person_name')
    if not name:
        return name
    if len(name.strip()) < 2:
        raise forms.ValidationError("Name must be at least 2 characters long.")
    return name.strip()