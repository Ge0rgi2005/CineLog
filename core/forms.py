from django import forms


class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="I confirm I want to delete this permanently.",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        error_messages={
            'required': 'You must confirm before deleting.',
        }
    )