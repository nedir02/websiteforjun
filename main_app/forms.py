from django import forms
from .models import Order, Customer, Service

class OrderForm(forms.ModelForm):  # Corrected: ModelForm instead of Modelform
    class Meta:
        model = Order
        fields = ['service']  # No need for customer in the form; we'll set it in the view.
        widgets = {
            # The 'customer' field can be hidden if it's being set in the view
            'customer': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()  # List all services

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']