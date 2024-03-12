from django.contrib import admin
from .base_admin import BaseAdmin
from django_select2.forms import Select2Widget, Select2MultipleWidget
from django import forms
from ..model_classes import (
    Book,
    Genre,
)


class BookAdminForm(forms.ModelForm):
    # Define a custom field for genres
    genres_form_field = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=Select2MultipleWidget(
            attrs={
                'class': 'select2',
                'data-width': '100%',
                'data-placeholder': 'Select genres',
                'data-show-all': True,
            },
        ))

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'author': Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genres_form_field'].label = "Genres"
        # If instance exists, populate genres field with instance's genres
        if self.instance and self.instance.pk:
            self.fields['genres_form_field'].initial = self.instance.genres.all()

    def save(self, commit=True):
        # Save the form instance
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            # Update the genres relationship manually
            instance.genres.set(self.cleaned_data['genres_form_field'])
        return instance

    class Media:
        css = {
            'all': ('css/model_multiple_choice_field.css',),
        }


class BookAdmin(BaseAdmin):
    # Use the custom form
    form = BookAdminForm

    fields = (
        'author',
        'genres_form_field',
        'title',
        'description',
        'rating',
        'published_date',
        'status',
    )


admin.site.register(Book, BookAdmin)
