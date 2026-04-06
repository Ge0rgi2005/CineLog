from django import forms
from .models import Review, ReviewComment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'body', 'rating', 'film')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your review a title',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your full review here...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Rate from 1 to 10',
            }),
            'film': forms.HiddenInput(),
        }
        labels = {
            'title': 'Review Title',
            'body': 'Your Review',
            'rating': 'Rating (1-10)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['film'].disabled = True

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if not body:
            return body
        if len(body.strip()) < 10:
            raise forms.ValidationError(
                "Your review must be at least 10 characters long."
            )
        return body.strip()

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating:
            return rating
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            return title
        if len(title.strip()) < 3:
            raise forms.ValidationError(
                "Review title must be at least 3 characters."
            )
        return title.strip()


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
            }),
        }
        labels = {
            'body': 'Comment',
        }

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if not body:
            return body
        if len(body.strip()) < 2:
            raise forms.ValidationError(
                "Comment must be at least 2 characters long."
            )
        return body.strip()