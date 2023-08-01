from django import forms
from django.forms import ModelForm
from .models import account, gen_otp, login
from django.core.validators import RegexValidator
import re
import hashlib

# reference: https://stackoverflow.com/questions/40224136/django-save-form-data-to-database
# register form
class NewUserForm(ModelForm):
    first_name = forms.CharField(required=True, max_length=50, validators=[RegexValidator(regex='^[A-Za-z]+$')])
    last_name = forms.CharField(required=True, max_length=50, validators=[RegexValidator(regex='^[A-Za-z]+$')])
    country_code = forms.ChoiceField(choices = [('SG', 'SG'), ('ID', 'ID')])
    phone_number = forms.IntegerField(required=True, validators=[RegexValidator(regex='^[0-9]{8,11}$')])
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, max_length=30)
    password = forms.CharField(required=True, widget=forms.PasswordInput, max_length=20)
    retype_password = forms.CharField(required=True, widget=forms.PasswordInput, max_length=100) 
    
    class Meta:
        model = account
        fields = "__all__"

    # reference: https://stackoverflow.com/questions/38979919/django-password-and-password-confirmation-validation
    # when the form is submitted, the form will be cleaned
    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        password = cleaned_data.get('password')
        retype_password = cleaned_data.get('retype_password')
        username = cleaned_data.get('username')
        
        #check for special characters
        specialChar = re.compile('!@#$%^&*()<>?/|}{~:;,.<>')
        # checks if the password is less than 8 characters long 
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")

        # checks if there's any number inputted in the password
        if sum(num.isdigit() for num in password) < 1:
            raise forms.ValidationError ("Password must include numbers")
            
        # checks if there's uppercase letters used in the password
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must include uppercase characters")

        # checks if there's lowercase letters used in the password 
        if not any(char.islower() for char in password):
           raise forms.ValidationError("Password must include lowercase characters")
        
        # checks if password includes special characters
        if specialChar.search(password) == None:
            raise forms.ValidationError("Password must include special characters")

        # checks if username is less than 8 characters long
        if len(username) < 8:
            raise forms.ValidationError("Username must be at least 8 characters")

        # checks if there's any number inputted in the username
        if sum(num.isdigit() for num in username) < 1:
            raise forms.ValidationError ("Username must include numbers")
            
        # checks if the user inputs any uppercase letters for the username
        if not any(char.isupper() for char in username):
            raise forms.ValidationError("Username must include uppercase characters")

        # checks if the user inputs any lowercase letters for the username
        if not any(char.islower() for char in username):
           raise forms.ValidationError("Username must include lowercase characters")

        # checks if the user inputs any special characters for the username
        if specialChar.search(username) == None:
            raise forms.ValidationError("Username must include special characters")
        
        # checks if the retype password and password have the same input 
        if password and retype_password:
            if password != retype_password:
                raise forms.ValidationError("Two password field don't match")
        return cleaned_data

# form used for the otp page
class otpForm(forms.Form):
    number = forms.CharField(required=True, max_length=6)
    class Meta: 
        model = gen_otp

# form used for the login page 
class LoginForm(forms.Form):
    input_usrname = forms.CharField(required=True, max_length=30)
    input_password = forms.CharField(required=True, widget=forms.PasswordInput, max_length=20)
    
    class Meta:
        model = login
