from django import forms
from .models import Product, Version


class ProductForm(forms.ModelForm):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in self.forbidden_words:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Название не может содержать запрещённое слово: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in self.forbidden_words:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"Описание не может содержать запрещённое слово: {word}")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
