from django import forms
from .models import Review, ReviewComment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'body', 'rating', 'movie')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title of your review goes here',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Your full written review goes here',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Your rating (1-10) goes here',
            }),
            'movie': forms.HiddenInput(),
        }
        labels = {
            'title': 'Review Title',
            'body': 'Your Review',
            'rating': 'Rating (1-10)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].disabled = True

def clean_review_body(self):
    review_body = self.cleaned_data.get('body')
    if not review_body:
        return review_body
    if len(review_body.strip()) < 10:
        raise forms.ValidationError("Your review must be at least 10 characters long.")
    return review_body.strip()

def clean_rating(self):
    rating = self.cleaned_data.get('rating')
    if not rating:
        return rating
    if rating < 1 or rating > 10:
        raise forms.ValidationError("Your rating must be on scale of 1-10.")
    return rating

def clean_title(self):
    title = self.cleaned_data.get('title')
    if not title:
        return title
    if len(title.strip()) < 3:
        raise forms.ValidationError("The title of your review must be at least 3 characters.")
    return title.strip()


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your comment goes here',
            }),
        }
        labels = {
            'body': 'Comment',
        }

def clean_comment_body(self):
    comment_body = self.cleaned_data.get('body')
    if not comment_body:
        return comment_body
    if len(comment_body.strip()) < 2:
        raise forms.ValidationError("Comment must be at least 2 characters long.")
    return comment_body.strip()