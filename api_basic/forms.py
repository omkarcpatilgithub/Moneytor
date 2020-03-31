from django import forms
from .models import Article
from crispy_forms.layout import Layout, Submit
from crispy_forms.helper import FormHelper



class HotelForm2(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('room', 'book_date','name')

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'
