from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
                'placeholder': 'Your email address goes here',
                'class': 'form-control',
            }),
        help_text='It is our solemn promise that we will never share your email with anyone else',
    )

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'confirm_password')
        widgets = {
            'username': forms.TextInput ( attrs={
                'placeholder': 'Get your inner hero on and choose a username',
                'class': 'form-control',
            } ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'placeholder': 'The stronger your password, the better',
            'class': 'form-control',
        })
        self.fields['confirm_password'].widget.attrs.update({
            'placeholder': 'Confirm your password just to be safe',
            'class': 'form-control',
        })
        self.fields['password'].help_text = "Password must be at least 8 characters long"
        self.fields['confirm_password'].help_text = "Enter your password again"

def clean_email(self):
    email = self.cleaned_data.get('email')
    if not email:
        return email
    if UserModel.objects.filter(email=email).exists():
        raise forms.ValidationError("An account with this email already exists.")
    return email

def clean_username(self):
    username = self.cleaned_data.get('username')
    if not username:
        return username
    if len(username) < 3:
        raise forms.ValidationError("Username must be at least 3 characters long.")
    if not username.isalnum():
        raise forms.ValidationError("Username can only contain letters and numbers.")
    return username

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
        }),
    )

    error_messages = {
        'invalid_login': "Incorrect username/password. Don't worry, you can try again.",
        'inactive': "This account has been disabled. What a bummer!",
    }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_avatar', 'favourite_genre')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your last name',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Introduce yourself to fellow Cineloggers',
            }),
            'favourite_genre': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'profile_avatar': 'Profile Picture',
            'favourite_genre': 'Favourite Genre',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['email'].help_text = "If you want to change your email, contact Support to do so."