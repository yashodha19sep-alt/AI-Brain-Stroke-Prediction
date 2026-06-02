from django import forms
from .models import User


class SignupForm(forms.ModelForm):

    # Gender Choices
    GENDER_CHOICES = [
        ('', '-- Select Gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    # Confirm Password Field
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'signup-input',
                'placeholder': 'Confirm Password'
            }
        )
    )

    # Gender Field
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'signup-input'
            }
        )
    )

    class Meta:
        model = User

        fields = [
            'firstname',
            'lastname',
            'phone',
            'email',
            'password',
            'gender',
            'dob'
        ]

        widgets = {

            'firstname': forms.TextInput(
                attrs={
                    'class': 'signup-input',
                    'placeholder': 'Enter First Name'
                }
            ),

            'lastname': forms.TextInput(
                attrs={
                    'class': 'signup-input',
                    'placeholder': 'Enter Last Name'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'signup-input',
                    'placeholder': 'Enter Phone Number'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'signup-input',
                    'placeholder': 'Enter Email'
                }
            ),

            'password': forms.PasswordInput(
                attrs={
                    'class': 'signup-input',
                    'placeholder': 'Enter Password'
                }
            ),

            'dob': forms.DateInput(
                attrs={
                    'class': 'signup-input',
                    'type': 'date'
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )

        return cleaned_data