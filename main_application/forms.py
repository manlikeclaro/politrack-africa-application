from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'full name', 'required': True}))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email address', 'required': True}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'email subject', 'required': True}))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'message', 'required': True}))
