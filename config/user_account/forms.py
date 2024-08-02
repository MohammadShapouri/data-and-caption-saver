from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from .models import UserAccount
from .utils.validators.username_validator import custom_ASCII_username_validator
# from django.utils.html import format_html


user_model = get_user_model()


class UserAccountCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
        self.fields['last_name'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
        self.fields['username'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
        self.fields['email'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
        self.fields['password1'].widget = forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"})
        self.fields['password2'].widget = forms.TextInput(attrs={"type": "password", "label": "Repeat Password", "class": "form-control", "placeholder": "Repeat Password"})
        # self.fields['username'].error_messages = {'unique': "This username is already in use."}
        # self.fields['email'].error_messages = {'unique': "This email is already in use."}
        # self.fields['password1'].help_text = format_html("<ul>  <li>{}</li> <li>{}</li> <li>{}</li>  <ul>".format(
        #                                                     "Something goes here",
        #                                                     "Something goes here",
        #                                                     "Something goes here"
        #                                                     )
        #                                                 )


    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email']


    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        try:
            user_model.objects.get(username__iexact = username)
        except user_model.DoesNotExist:
            return username
        else:
            if self.form_request.user.username == username:
                return username
            else:
                raise forms.ValidationError([{'username' : "This username is already in use."}])


    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        try:
            user_model.objects.get(email__iexact = email)
        except user_model.DoesNotExist:
            return email
        else:
            if self.form_request.user.email == email:
                return email
            else:
                raise forms.ValidationError([{'email' : "This email is already in use."}])





class LoginForm(forms.Form):
    username_email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username or Email"}), required=True, label="Username or Email", error_messages={'required': "This field is required. Don't leave it empty"})
    password = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"}), label="Password", error_messages={'required': "This field is required. Don't leave it empty"})


    def clean_username_email(self):
        cleaned_data = super().clean()
        username_email = cleaned_data.get('username_email')

        if str(username_email).__contains__('@'):
            email = username_email
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError([{ 'username_email' : "Email doesn't have correct structure."}])
            return email
        else:
            username = username_email
            try:
                custom_ASCII_username_validator(username)
            except forms.ValidationError:
                raise forms.ValidationError([{'username_email' : "Username doesn't have correct structure."}])
            return username





class UserAccountUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
        self.fields['last_name'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
        self.fields['username'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
        self.fields['email'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
        self.fields['username'].error_messages = {'unique' : "This username is already in use."}
        self.fields['email'].error_messages = {'unique' : "This email is already in use."}



    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture', 'is_private', 'is_discoverable']


    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        try:
            user_model.objects.get(username__iexact = username)
        except user_model.DoesNotExist:
            return username
        else:
            if self.form_request.user.username == username:
                return username
            else:
                raise forms.ValidationError([{'username' : "This username is already in use."}])


    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        try:
            user_model.objects.get(email__iexact = email)
            # user_model.objects.get(new_email__iexact = email)
        except user_model.DoesNotExist:
            return email
        else:
            if self.form_request.user.email == email or self.form_request.user.new_email == email:
                return email
            else:
                raise forms.ValidationError([{'email' : "This email is already in use."}])





class UserAccountDeletionForm(forms.Form):
    password = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"}), label="Password", error_messages={'password' : "Password doesn't have correct structure."})





class PasswordChangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"}), label="New Password")
    new_password2 = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"}), label="Repeat New Password")


    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        errors_dict = dict()


        if not self.form_request.user.check_password(old_password):
            errors_dict['old_password'] = "Your old password was entered incorrectly. Please enter it again."
        if new_password1 != new_password2:
            errors_dict['new_password2'] = "Two passwords aren't the same."
    
        try:
            # Validate the password and catch the exception
            validate_password(password=new_password1, user=self.form_request.user)
        # The exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors_dict['new_password1'] = list(e.messages)

        if errors_dict:
            raise forms.ValidationError(errors_dict)
        return super().clean()





class PasswordResetForm(BasePasswordResetForm):
    username_email = forms.CharField(required=True, label="Username or Email", error_messages={'required': "This field is required. Don't leave it empty"})


    def clean_username_email(self):
        cleaned_data = super().clean()
        username_email = cleaned_data.get('username_email')

        if str(username_email).__contains__('@'):
            email = username_email
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError([{ 'username_email' : "Email doesn't have correct structure."}])
            return email
        else:
            username = username_email
            try:
                custom_ASCII_username_validator(username)
            except forms.ValidationError:
                raise forms.ValidationError([{'username_email' : "Username doesn't have correct structure."}])
            return username
