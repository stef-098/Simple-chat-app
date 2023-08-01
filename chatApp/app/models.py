from django.db import models
from datetime import datetime


# user account's model database
class account(models.Model):
    first_name = models.fields.CharField(max_length=50)
    last_name = models.fields.CharField(max_length=50)
    country_code = models.fields.CharField(max_length=5)
    phone_number = models.fields.IntegerField()
    email = models.fields.EmailField(default='',max_length=50)
    username = models.fields.CharField(max_length=30)
    password = models.fields.CharField(max_length=100)


    def __str__(self):
        return f'{self.username}'

# generating otp model database
class gen_otp(models.Model):
    number = models.fields.CharField(max_length=6)

    def __str__(self):
        return f'{self.number}'

# login user account model database
class login(models.Model):
    input_username = models.fields.CharField(max_length=30)
    input_password = models.fields.CharField(max_length=100)
    time = models.fields.DateTimeField(auto_now_add = True)

    class Meta: 
        get_latest_by = 'time'

    def __str__(self):
        return f'{self.input_username}'

# chat messages model database 
class Message(models.Model):
    conversation = models.CharField(max_length=100000)
    username = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.conversation}'
