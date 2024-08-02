from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"})
        self.fields['description'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Description"})


    class Meta:
        model = Album
        fields = ['name', 'description', 'album_picture', 'is_private']





class AlbumDeletionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    password = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "label": "Password", "class": "form-control", "placeholder": "Password"}), label="Old Password")
    want_to_delete_data = forms.BooleanField(label="Do you wnat to delete all data of this album.", required=False)


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        errors_dict = dict()

        if not self.form_request.user.check_password(password):
            errors_dict['password'] = "Your password was entered incorrectly. Please enter it again."

        if errors_dict:
            raise forms.ValidationError(errors_dict)
        return super().clean()

