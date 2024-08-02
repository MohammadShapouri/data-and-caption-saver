from django import forms
from django.db.models import Q
from .models import DataAndCaption
from album.models import Album



class DataAndCaptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": self.fields['title'].label})
        self.fields['url'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": self.fields['url'].label})
        self.fields['owner_description'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": self.fields['owner_description'].label})
        self.fields['ai_based_description'].widget = forms.TextInput(attrs={"class": "form-control", "placeholder": self.fields['ai_based_description'].label})
        self.fields['album'].queryset = Album.objects.filter(Q(owner = self.form_request.user) & ~Q(name = 'DELETED_DATA_ALBUM'))

    class Meta:
        model = DataAndCaption
        fields = ['title', 'file', 'url', 'owner_description', 'ai_based_description', 'album']
    
    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')

        print(cleaned_data)
        print(self.form_request.FILES)
        print(url == None)
        print(bool(self.form_request.FILES))
        print(bool(self.form_request.FILES) == False)
               
        if url == None and bool(self.form_request.FILES) == False:
            raise forms.ValidationError({'file': "Either upload a file or paste a link."})
        return super().clean()