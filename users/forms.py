from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import Item
from .models import ConversationMessages, Conversation

class UserRegisterForm(UserCreationForm):
    email  = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'image']
        
class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'is_sold']
        
class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessages
        fields =['content',]