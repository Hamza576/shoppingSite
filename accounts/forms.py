from django import forms
from accounts.models import User, UserProfile
from django.contrib.auth.hashers import check_password

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Both Passwords doesn't matched.")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not check_password(password, user.password):
                    self.add_error("password", "You entered Incorrect Password. Try Again!")             
            except User.DoesNotExist:
                self.add_error("email", "No Account was associated with this Email Address.")

        return cleaned_data

class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No Account was associated with this Email Address.")
        
        return email

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'state', 'country', 'address'] 
