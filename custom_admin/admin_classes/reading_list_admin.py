from django.contrib import admin
from .base_admin import BaseAdmin
from django_select2.forms import Select2Widget, Select2MultipleWidget
from django import forms
from ..model_classes import (
    ReadingList,
    Book,
    CustomUser,
)


class ReadingListAdminForm(forms.ModelForm):
    # Define a custom field for books
    books_form_field = forms.ModelMultipleChoiceField(
        queryset=Book.objects.all(),
        required=False,
        widget=Select2MultipleWidget(
            attrs={
                'class': 'select2',
                'data-width': '100%',
                'data-placeholder': 'Select books',
                'data-show-all': True,
            },
        ))

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'user': Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['books_form_field'].label = "Books"
        # If instance exists, populate books field with instance's books
        if self.instance and self.instance.pk:
            self.fields['books_form_field'].initial = self.instance.books.all()
        self.fields['user'].widget.choices = [
            (user.pk, str(user)) for user in CustomUser.objects.filter(is_staff=False, is_superuser=False)
        ]

    def save(self, commit=True):
        # Save the form instance
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            # Update the books relationship manually
            instance.books.set(self.cleaned_data['books_form_field'])
        return instance

    class Media:
        css = {
            'all': ('css/model_multiple_choice_field.css',),
        }


class ReadingListAdmin(BaseAdmin):
    form = ReadingListAdminForm
    fields = (
        'user',
        'books_form_field',
        'name',
        'status',
    )


admin.site.register(ReadingList, ReadingListAdmin)
