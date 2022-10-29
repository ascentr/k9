from django import forms

class Contacts_form(forms.Form):

    from_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': ''}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': ''}))
    message = forms.CharField(required=True, widget=forms.Textarea)

    