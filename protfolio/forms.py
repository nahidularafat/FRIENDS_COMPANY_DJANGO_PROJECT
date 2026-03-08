# file path: protfolio/forms.py
from .models import Developer, Review, Service, BlogPost, Client, ContactInfo
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.HiddenInput()
        }

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'position', 'experience', 'image', 'bio', 'linked_in_url']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'icon_class', 'image']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'logo', 'website_url', 'display_order']

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['address', 'phone', 'whatsapp', 'email']        