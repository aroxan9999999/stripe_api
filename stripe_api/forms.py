from django import forms

class Add_order_form(forms.Form):
    order_id = forms.CharField(max_length=1)