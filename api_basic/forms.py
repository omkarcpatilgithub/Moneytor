from django import forms
from django.forms import DateInput
from .models import Article
from crispy_forms.layout import Layout, Submit
from crispy_forms.helper import FormHelper

class DatePicker (forms.DateInput):
    input_type = 'date'


class HotelForm(forms.ModelForm):
    class Meta:
        ## TODO learn more about widgets
        widgets = {'book_date': DatePicker()}       # should thank this video https://www.youtube.com/watch?v=I2-JYxnSiB0
        model = Article
        fields = ('room', 'book_date','name')

    helper = FormHelper()   ## not part of Meta class, always keep outside of it
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))          ## adds in the list of layout, all the mentioned fields are already added
    helper.form_method = 'POST'


class CheckAvailabilityForm(forms.Form):
    start_date = forms.DateField(widget=DatePicker())
    end_date   = forms.DateField(widget=DatePicker())
    #name = forms.CharField(max_length=20)

    helper = FormHelper()  ## not part of Meta class, always keep outside of it
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))  ## adds in the list of layout, all the mentioned fields are already added
    helper.form_method = 'POST'

class MultiBookingForm(forms.Form):

    room = forms.IntegerField(initial= 101, min_value=101, max_value=110)
    start_date = forms.DateField(widget=DatePicker())
    end_date   = forms.DateField(widget=DatePicker())
    name = forms.CharField(max_length=20)

    helper = FormHelper()  ## not part of Meta class, always keep outside of it
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))  ## adds in the list of layout, all the mentioned fields are already added
    helper.form_method = 'POST'


class CancelBookingForm(forms.Form):
    room_Number = forms.IntegerField(initial=101, min_value=101, max_value=110)
    date_of_booking = forms.DateField(widget=DatePicker())
    helper = FormHelper()  ## not part of Meta class, always keep outside of it
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))  ## adds in the list of layout, all the mentioned fields are already added
    helper.form_method = 'POST'