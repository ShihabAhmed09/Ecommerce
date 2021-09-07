from django import forms
from django.contrib.auth.models import User
from .models import Customer, Contact, Feedback, Product, Order, ShippingAddress


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name'}


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        labels = {'profile_pic': 'Profile Picture'}
        exclude = ['user']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'digital', 'featured', 'image', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control mt-1', 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['tags'].empty_label = 'Select Category'


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['customer', 'order', 'date_added']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'First Name*'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Last Name*'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Mobile*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Email*'}),
            'address': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Address*'}),
            'city': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'City*'}),
            'division': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Division*'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'feedback']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-1'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control mt-1', 'rows': 6}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-1', 'placeholder': 'name@example.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control mt-1', 'placeholder': 'Message',
                                             'rows': 6}),
        }
