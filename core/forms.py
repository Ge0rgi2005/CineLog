from django import forms


class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="I confirm to permanently deleting this.",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        error_messages={
            'required': 'Are you sure of your confirmation? Once you do so, there is no going back.',
        }
    )