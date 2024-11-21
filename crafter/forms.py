from django import forms
from django.forms import formset_factory


class CourseForm(forms.Form):
    shortname = forms.CharField(
        label='Short name',
        widget=forms.TextInput(attrs={'placeholder': 'Short name'})
    )
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'placeholder': 'Title'})
    )

class CourseLinkForm(forms.Form):
    url = forms.URLField(
        label='URL',
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter a URL'})
    )

# Create a formset
CourseLinkFormSet = formset_factory(CourseLinkForm, extra=3, max_num=2, min_num=1)