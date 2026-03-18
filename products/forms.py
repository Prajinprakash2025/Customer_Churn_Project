from django import forms
from .models import SellerRequest

class SellerRequestForm(forms.ModelForm):
    class Meta:
        model = SellerRequest
        fields = ['store_name','phone']