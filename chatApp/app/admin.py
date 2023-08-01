from django.contrib import admin
from .models import account, gen_otp, Message, login

# Register your models here.

class accountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'country_code', 'email', 'phone_number', 'username', 'password')

class gen_otpAdmin(admin.ModelAdmin):
    list_display = ['number']

class MessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'conversation')

class loginAdmin(admin.ModelAdmin):
    list_display = ('input_username', 'input_password')

admin.site.register(login, loginAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(account, accountAdmin)
admin.site.register(gen_otp, gen_otpAdmin)