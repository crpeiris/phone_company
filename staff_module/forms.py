from django import forms
from .models import Staff, Role
from store.models import Order,Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'more_info', 'image', 'is_sale', 'sale_price']


        

class StaffRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    telephone = forms.CharField(max_length=15)

    class Meta:
        model = Staff
        fields = ['username', 'email', 'telephone']  # Removed password fields

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'permissions']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Include all fields from the Product model in the form
        fields = [
            'name', 'price', 'category', 'description', 
            'more_info', 'image', 'is_sale', 'sale_price'
        ]
        widgets = {
            # Use Textarea for description and more_info to allow multi-line input
            'description': forms.Textarea(attrs={'rows': 3}),
            'more_info': forms.Textarea(attrs={'rows': 5}),
        }

    # Custom validation to enforce business rules
    def clean(self):
        cleaned_data = super().clean()  # Get the cleaned data from the form
        is_sale = cleaned_data.get('is_sale')  # Check if the product is on sale
        sale_price = cleaned_data.get('sale_price')  # Sale price entered by the user
        price = cleaned_data.get('price')  # Original price of the product

        # If the product is marked for sale, ensure the sale price is less than the original price
        if is_sale and sale_price >= price:
            # Add an error to the sale_price field if the condition is not met
            self.add_error('sale_price', "Sale price must be less than the original price.")

        return cleaned_data  # Return the cleaned data after validation
