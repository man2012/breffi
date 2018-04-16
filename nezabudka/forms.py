# forms.py
from django.core.exceptions import ValidationError
from django import forms
import json

from .models import Import
from .models import Contacts
from .validators import validate_file_extension, validate_phone, validate_email


class ContactViewForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['name', 'company', 'email', 'phone', 'interest']
        exclude = ('pk',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                            'placeholder': 'Vladimir',
                            'data-error':'',
                            'required':'required',
                            }),
            'company': forms.TextInput(attrs={'class': 'form-control',
                            'placeholder': 'Yandex',
                            'data-error':'',
                            'required':'required',
                            }),
            'interest': forms.TextInput(attrs={'class': 'form-control',
                            'placeholder': 'I love game in computer',
                            'data-error':'',
                            'required':'required',
                            }),
            'email': forms.EmailInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'user@user.ru',
                            'required':'required',
                            }),
            'phone': forms.TextInput(attrs={'class': 'form-control',
                            'placeholder': '81234567891',
                            'data-error':'',
                            'required':'required',
                            }),
        }

    def clean_phone(self):
        value = self.cleaned_data.get('phone', False)
        validate_phone(value)
        return value

    def clean_email(self):
        value = self.cleaned_data.get('email', False)
        validate_email(value)
        return value


class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = Import
        fields = ['myfile']
        widgets = {
            'myfile': forms.FileInput(attrs={'accept': '.json, application/json'}),
        }

    def clean_myfile(self):
        value = self.cleaned_data.get('myfile', False)
        validate_file_extension(value)
        value.seek(0)
        data = value.read()
        data = json.loads(data.decode('utf-8'))

        for d1 in data:
            form = ContactViewForm(d1)

            if form.is_valid():
                form.save()

        return value
