from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FlightBooking




class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control .w-100', 'readonly': 'readonly'}),
            'product': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_of_ticket': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'adults': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
            'children': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infants': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'travel_class': forms.Select(attrs={'class': 'form-control'}),
            
            'accommodation': forms.Select(attrs={'class': 'form-control'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control .w-150'}),
            'promo_code': forms.TextInput(attrs={'class': 'form-control'}),
            'extra_fee': forms.TextInput(attrs={'class': 'form-control', 'style':'display:none'}),
            
            'status': forms.Select(attrs={})
        }

def clean(self):
    cleaned_data = super().clean()
    
    # Calculate extra_fee based on accommodation type
    accommodation = cleaned_data.get('accommodation')
    extra_fee = 0.00

    if accommodation == 'Hotel':
        extra_fee = 100.00
    elif accommodation == 'Apartment':
        extra_fee = 150.00
    elif accommodation == 'Villa':
        extra_fee = 200.00

    cleaned_data['extra_fee'] = extra_fee
    
    # Validate dates and product availability
    departure_date = cleaned_data.get("departure_date")
    return_date = cleaned_data.get("return_date")
    product = cleaned_data.get('product')

    if product and product.is_sold_out():
        raise forms.ValidationError("This product is sold out.")

    if return_date and return_date < departure_date:
        self.add_error('return_date', "Return date cannot be before the departure date.")

    return cleaned_data

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'type'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'id': 'typeEmailX', 'type': 'email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id':"typePasswordX", 'type': 'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id':"typePassword", 'type': 'password'}),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['username', 'user', 'date_created', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'country': forms.Select(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m', 'type': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'about': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example1m'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg bg-info', 'id': 'form3Example1m'}),

        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'




class FlightBookingForm(forms.ModelForm):
    class Meta:
        model = FlightBooking
        fields = [
            'full_name', 'date_of_birth', 'gender', 'contact_email', 'contact_phone',
            'departure_city', 'destination_city', 'departure_date', 'return_date',
            'travel_class', 'num_adults', 'num_children', 'num_infants',
            'preferred_airline', 'seat_preference', 'meal_preference',
            'extra_baggage', 'travel_insurance', 'airport_transfers', 'special_assistance'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'departure_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departure City'}),
            'destination_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination City'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'travel_class': forms.Select(attrs={'class': 'form-control'}),
            'num_adults': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'num_children': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'num_infants': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'preferred_airline': forms.Select(attrs={'class': 'form-control'}),
            'seat_preference': forms.Select(attrs={'class': 'form-control'}),
            'meal_preference': forms.Select(attrs={'class': 'form-control'}),
            'extra_baggage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'travel_insurance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'airport_transfers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'special_assistance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Custom validations if necessary
    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get("departure_date")
        return_date = cleaned_data.get("return_date")

        if return_date and return_date < departure_date:
            self.add_error('return_date', "Return date cannot be before the departure date.")

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea,)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "spam" in email:
            raise forms.ValidationError("We do not accept emails from spam.com.")
        return email
    
class RecoveryKeyRequestForm(forms.ModelForm):
    class Meta:
        model = RecoveryKeyRequest
        fields = ['username', 'social_media_account', 'last_used_password', 'id_card_upload', 'contact_method']
        widgets = {
            'last_used_password': forms.PasswordInput(),
        }

    def clean_contact_method(self):
        contact = self.cleaned_data.get('contact_method')
        if '@' in contact:
            if not forms.EmailField().clean(contact):
                raise forms.ValidationError("Enter a valid email address.")
        return contact


from django import forms

class PaymentForm(forms.Form):
    key = forms.ModelChoiceField(queryset=DigitalKey.objects.all(), widget=forms.HiddenInput())
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), label="Choose Payment Method")
    card_number = forms.CharField(max_length=16, required=False, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    bank_transfer_reference = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bank Transfer Reference'}))
    crypto_wallet_address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Crypto Wallet Address'}))
    gift_card_code = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Gift Card Code'}))
    mobile_app_reference = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Mobile App Transfer Reference'}))

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method.name == 'bank_card' and not cleaned_data.get('card_number'):
            self.add_error('card_number', 'Card number is required for bank card payments.')
        if payment_method.name == 'bank_transfer' and not cleaned_data.get('bank_transfer_reference'):
            self.add_error('bank_transfer_reference', 'Bank transfer reference is required for bank transfer payments.')
        if payment_method.name == 'crypto' and not cleaned_data.get('crypto_wallet_address'):
            self.add_error('crypto_wallet_address', 'Crypto wallet address is required for cryptocurrency payments.')
        if payment_method.name == 'gift_card' and not cleaned_data.get('gift_card_code'):
            self.add_error('gift_card_code', 'Gift card code is required for gift card payments.')
        if payment_method.name == 'mobile_app' and not cleaned_data.get('mobile_app_reference'):
            self.add_error('mobile_app_reference', 'Mobile app transfer reference is required for mobile app transfers.')

        return cleaned_data

class GiftCardPaymentForm(forms.ModelForm):
    class Meta:
        model = GiftCardPayment
        fields = ['receipt_image', 'card_front_image', 'card_back_image', 'card_type', 'card_code']
        


class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Amount")

class HoldingForm(forms.Form):
    symbol = forms.CharField(max_length=10)
    amount = forms.DecimalField(max_digits=20, decimal_places=8)

    