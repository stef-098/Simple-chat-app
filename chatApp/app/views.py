from django.shortcuts import  render, redirect
from .forms import NewUserForm, LoginForm
from django.contrib import messages
from .models import account, gen_otp, login, Message
import hashlib
from random import randint
from twilio.rest import Client
from django.http import HttpResponse, JsonResponse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import json



# reference: https://stackoverflow.com/questions/32642061/how-do-i-compare-form-inputs-with-database-values-in-django

def key_gen():
    keypair = RSA.generate(3078)
    public_key = keypair.publickey()
    return public_key, keypair

#generates key for message encryption
pub_key = 0
private_key = 0
pub_key, private_key = key_gen()

# encrypts messages using public key
def encrypts(message, publickey):
    key = PKCS1_OAEP.new(publickey)
    encrypted = key.encrypt(message)
    return encrypted

# decrypt messahes using private key 
def decrypts(message, private_key):
    key = PKCS1_OAEP.new(private_key)
    decrypt = key.decrypt(message)

def Home(request):
    return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST':
        form =  NewUserForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            country_code = request.POST['country_code']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password = hashlib.sha256(password.encode()).hexdigest()
            user = account(first_name=first_name, last_name=last_name, country_code=country_code, phone_number=phone_number, email=email, username=username, password=password)
            user.save()

            return redirect('otp')
    else: 
        form = NewUserForm()
        messages.error(request, "Registration invalid!")
    return render(request=request, template_name="signup.html", context={'form':form})


# function to generate otp
def number_ver():
    verify = ''
    for i in range(6):
        verify += str(randint(0,9))
    return verify

def otp(request):
    # when the function is called to get the otp page, the function for generating the otp is also called  
    if request.method == 'GET':
        number = number_ver()
        # after the number is generated, it will be stored in the database 
        number1 = gen_otp.objects.create(number=number)
        account_sid = "ACb03dc33f53cf6875b577912b89004403" 
        auth_token = "4912b1b8e9cd555dda4c9858e30671b0" 
        client = Client(account_sid, auth_token)
        from_number = 'whatsapp:+14155238886'
        to_number = 'whatsapp:+6586951756'
        # twilio creates a message (otp) and send it to the phone number
        client.messages.create(
            body=f'your OTP: {number1}',
            from_=from_number,
            to=to_number)
    
    # when the user submits the form,   
    if request.method == 'POST':
        num = gen_otp.objects.last()
        # if the otp matches the one that is stored in the database, then it will redirect user to login page and deletes the OTP number egnerated from the database 
        if str(num) == request.POST['number']:
            num.delete()
            return redirect('login')
        else:
            # if the OTP iputted doesn't match the one that is stored in the database, it will show error message and deletes the OTP generated from the database 
            messages.error(request, "invalid OTP")
            num.delete()
            # deletes the account's registration 
            redirect('/')
    return render(request, "otp.html")


def Login(request): 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            input_username = request.POST["input_username"]
            input_password = request.POST["input_password"]
            # hashes the password the user inputs using sha256
            hashed_pass = hashlib.sha256(input_password.encode()).hexdigest()
            name = account.objects.all()
            try:             
                # checks if the username the user input is registered
                name = account.objects.get(username=input_username)
            except account.DoesNotExist:
                # if username isn't registered, it will display error message and will redirect user to homepage.html
                messages.error(request, "Wrong username inputted!")
                return redirect('/')
            passw = account.objects.all()
            try: 
                # checks if the password the user input is registered
                passw = account.objects.get(password=hashed_pass)
                # if username isn't registered, it will display wrror message and will redirect user to main.html
            except account.DoesNotExist:
                messages.error(request, "Wrong password inputted!")
                return redirect('/')
            # if both password and username is valid, then the 
            logins = login(input_username=input_username, input_password=hashed_pass)
            print(logins)
            logins.save()
            return redirect ('convo')
    else: 
        form = LoginForm()
        messages.error(request, "User not found!")
        username = request.GET.get('username')
    return render(request=request, template_name="login.html", context={'form':form})

def convo(request):    
    username = login.objects.latest('input_username')
    return render(request, template_name='conversation.html', context={'user': username})

# send messages function
def send(request):
    unencrypted_msg = request.POST['message']
    username = request.POST['username']
    #encode the unencrypted message
    msg = unencrypted_msg.encode()
    message = encrypts(msg, pub_key)
    # the message will be stored into the database encrypted using RSA
    new_msg = Message(conversation=message, username=username)
    new_msg.save()
    return HttpResponse("Message sent!")

# get sent messages from the database into the chatroom
def getMessages(request):
    text=[]
    messages = Message.objects.all()
    # decrypting messages into plaintext
    # ciphertext_list = list(ciphertext)
    # for msg in ciphertext_list:
    #      text = decode(msg)
    # messages = decrypts(text, private_key)
    #return all values of messages
    return JsonResponse({"messages":list(messages.values())})


def Logout(request):
    return render(request, template_name='logout.html')
