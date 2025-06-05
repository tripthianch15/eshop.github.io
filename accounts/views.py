from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from django.conf import settings
from random import randint

from .forms import SignupForm, SigninForm,OTPForm
from .models import CustomUser, Buyer, Seller, UserKYC
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
# Create your views here.

def buyer_signup_view(request):
    #request.session['user_type'] = 'buyer'
    print("buyer_signup_view")
   
    if request.method == "POST":
        first_name = request.POST["first_name"]
        login_user_id = request.POST["login_user_id"]
        email = request.POST["email"]
        #password = request.POST["password"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if (password1 != password2):             
             error_message = f'Passwords do not match!'
             #messages.info(request,error_message)
             
             return (pass_entered_data(request,error_message))
        else:
             userObj = CustomUser.objects.filter(username=login_user_id)
             if userObj.exists():  # checks if an email exists
                 messages.error(request, f"The login user id {login_user_id} exists", fail_silently=True)
    
                 username = userObj[0].username
                 error_message = f"Login User ID: {username} already used, Use a different Login User ID"
                 return(pass_entered_data(request,error_message))
       
             else:
                 #print("no user")        
                 error_message =''
                 contact_number = request.POST["contact_number"]
                            
                 # Create User with Delete flag = 'Y'
                 # Later if entered OTP matches with the generate OTP
                 # Change the deleted flag = 'Y' (By default it is 'Y')
                 # Once it is confirmed using OTP change deleted to 'N'
                 
                 new_user = CustomUser.objects.create_user(username=login_user_id,
                 first_name=first_name, email=email,contact_number=contact_number,
                 user_type="buyer")
                 new_user.set_password(password1)
                 #new_user.user_type = user_type
                 new_user.save()
                 request.session['password'] = password1
                 # Generate OTP and Send OTP
                 # generate_and_send_otp function is called 
                 # to Send OTP 
                 request.session['email'] = new_user.email
                 request.session['retry_otp'] = 'no'
                 request.session['otp_message'] = 'OTP has been sent to registerd email ID.'
                 request.session['user'] = new_user.username
                 #IF OTP is required remove below comment from below two lines
                 # and comment  return create_user_Profile_and_authenticate(request)

                 generate_and_send_otp(request)
                 return display_otp_page(request)
                 #return create_user_profile_and_authenticate(request,new_user)
                 #return redirect('/index/')
    else:# GET
        form = SignupForm()
        return render(request, 'accounts/buyer_signup.html', {'form': form})


def seller_registration_view(request):
   
   print("seller_registration_view")
   if request.method == "POST":
        first_name = request.POST["first_name"]
        login_user_id = request.POST["login_user_id"]
        email = request.POST["email"]
        #password = request.POST["password"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if (password1 != password2):             
             error_message = f'Passwords do not match!'
             #messages.info(request,error_message)
             
             return (pass_entered_data(request,error_message))
        else:
             userObj = CustomUser.objects.filter(username=login_user_id)
             if userObj.exists():  # checks if an email exists
                 messages.error(request, f"The login user id {login_user_id} exists", fail_silently=True)
    
                 username = userObj[0].username
                 error_message = f"Login User ID: {username} already used, Use a different Login User ID"
                 return(pass_entered_data(request,error_message))
       
             else:
                 #print("no user")        
                 error_message =''
                 contact_number = request.POST["contact_number"]
                            
                 # Create User with Delete flag = 'Y'
                 # Later if entered OTP matches with the generate OTP
                 # Change the deleted flag = 'Y' (By default it is 'Y')
                 # Once it is confirmed using OTP change deleted to 'N'
                 # new_user = User.objects.create_user(username=email,
                 #     first_name=first_name, email=email,contact_number=contact_number
                 #                 )
                 #user_type = request.session['user_type']
                 print("In signup_view")
                 new_user = CustomUser.objects.create_user(username=login_user_id,
                 first_name=first_name, email=email,contact_number=contact_number,
                 user_type="seller")
                 new_user.set_password(password1)
                 #new_user.user_type = user_type
                 new_user.save()
                 request.session['password'] = password1
                 # Generate OTP and Send OTP
                 # generate_and_send_otp function is called 
                 # to Send OTP 
                 request.session['email'] = new_user.email
                 request.session['retry_otp'] = 'no'
                 request.session['otp_message'] = 'OTP has been sent to registerd email ID.'
                 request.session['user'] = new_user.username
                 #IF OTP is required remove below comment from below two lines
                 # and comment  return create_user_Profile_and_authenticate(request)

                 generate_and_send_otp(request)
                 return display_otp_page(request)
                 #return create_user_profile_and_authenticate(request,new_user)
                 #return redirect('/index/')
   else:# GET
        form = SignupForm()
        return render(request, 'accounts/seller_signup.html', {'form': form})


# The below function is called from
# Signup_view when passwords do not match 
# or Loginuser ID already used

def pass_entered_data(request,error_message):
     
     data = request.POST
     username = data['login_user_id']
     
     user_form = SignupForm(request.POST)
     context = {'user_form': user_form, 'title': 'Create Account', 
                'login_user_id':data['login_user_id'],
                'email': data['email'],
                'first_name': data['first_name'],
                'contact_number': data['contact_number'],
                 #'domain':settings.DOMAIN,                 
                 'error_message':error_message}
     
     import re

     # Assuming data['contact_number'] is in the format +<country_code>xxxxxxxxxx
     contact_number = data['contact_number']

     # Check if the phone number starts with a '+' and has at least 12 characters
     if contact_number.startswith('+') and len(contact_number) >= 12:
                    # Extract the country code (one or more digits) and the last 10 digits using regex
                    #match = re.match(r'(\+\d+)(\d{10})$', contact_number)
          match = re.match(r'(\+\d[-\d]*)(\d{10})$', contact_number)
                    
          if match:
              country_code = match.group(1)  # This will be the country code, e.g., +123 or +91
              mobile_number = match.group(2)  # This will be the last 10 digits, e.g., 1234567890
          else:
              # Handle cases where the phone number format is not as expected
              country_code = None
              mobile_number = None
     else:
             # Handle cases where the phone number is invalid
         country_code = None
         mobile_number = None

     user_details = {"username":data['login_user_id'],
                     "full_name": data['first_name'], 
                     "email": data['email'],
                     #"selected_country_code": country_code,
                     "contact_number": mobile_number,
                     #"alternate_number": data['alt_contact_number'],
                     #"gender":data['gender'],
                     #"postal_address": data['postal_address'],             
                     #"pin_code": data['pin_code'],
                     #"district": data['district'],             
                     #"state": data['state'],  
                     #"country": data['country'],  
                     #"institute": data['institute'],  
                     #"date_of_birth": data['dob']
                     }
     
     context.update(user_details) 
     return render(request, "accounts/signup.html",context)

# This function renders a page to display a OTP page
def display_otp_page(request):
     
     # Display OTP entering form page
     otp_form= OTPForm()
     otp_message =  request.session['otp_message']
     retry_otp = request.session['retry_otp']
     user = request.session['user']
     #context = {'retry_otp':retry_otp,'otp_message':otp_message,'otp_form': otp_form, 'title': 'Enter OTP','domain':settings.DOMAIN}
     context = {'retry_otp':retry_otp,'otp_message':otp_message,'otp_form': otp_form,
                 'title': 'Enter OTP','user':user}
     
    #  title = get_title()
    #  context.update(title)    
    #  tenant = get_tenant()
    #  tenant_context = {'tenant': tenant}
    #  context.update(tenant_context)       
     #otp_form = AuthenticationForm()
     return render(request, "accounts/otp.html", 
                      context) 


from .forms import SigninForm
def buyer_login_view(request):
    """This is for signing in a user"""
    if request.method == "POST":
        login_user_id = request.POST["login_user_id"]
        password = request.POST["password"]
        print("login user id: ",login_user_id)
        print("password: ", password)
       
        user = auth.authenticate(request, username=login_user_id, password=password)
        context ={}
        if user is not None:
            context ={}
            print(f"Authenticated user: {user}")
            auth.login(request, user)
            # if user.user_type == 2:
            #     return redirect("/dashboard/")
            # else:

            #     return redirect("/")
          
            return redirect("/")
        
        else:
            context = {"error_message":"Invalid credentials or User doesn't exists"}
            print("Authentication failed")
            messages.error(
                request,
                "Invalid credentials or User doesn't exists",
                fail_silently=True, extra_tags='warning'
            )
        #print("User= ", user)
       #print("request.user", request.user)
    form = SigninForm()
    context = {"user_type": "Buyer"}
    return render(request, "accounts/login.html",context)

def seller_login_view(request):
    """This is for signing in a user"""
    if request.method == "POST":
        login_user_id = request.POST["login_user_id"]
        password = request.POST["password"]
        print("login user id: ",login_user_id)
        print("password: ", password)
       
        user = auth.authenticate(request, username=login_user_id, password=password)
        context ={}
        if user is not None:
            context ={}
            print(f"Authenticated user: {user}")
            auth.login(request, user)
            # if user.user_type == 2:
            #     return redirect("/dashboard/")
            # else:

            #     return redirect("/")
          
            return redirect("/admin/")
        
        else:
            context = {"error_message":"Invalid credentials or User doesn't exists"}
            print("Authentication failed")
            messages.error(
                request,
                "Invalid credentials or User doesn't exists",
                fail_silently=True, extra_tags='warning'
            )
        #print("User= ", user)
       #print("request.user", request.user)
    form = SigninForm()
    context = {"user_type": "Seller"}
    return render(request, "accounts/login.html",context)

def staff_login_view(request):
    """This is for signing in a user"""
    if request.method == "POST":
        login_user_id = request.POST["login_user_id"]
        password = request.POST["password"]
        print("login user id: ",login_user_id)
        print("password: ", password)
       
        user = auth.authenticate(request, username=login_user_id, password=password)
        context ={}
        if user is not None:
            context ={}
            print(f"Authenticated user: {user}")
            auth.login(request, user)
             
            return redirect("accounts/admin/")
        
        else:
            context = {"error_message":"Invalid credentials or User doesn't exists"}
            print("Authentication failed")
            messages.error(
                request,
                "Invalid credentials or User doesn't exists",
                fail_silently=True, extra_tags='warning'
            )
        #print("User= ", user)
       #print("request.user", request.user)
    form = SigninForm()
    context = {"user_type": "Staff"}
    return render(request, "accounts/login.html/",context)

def logout_view(request):
    """This is for logging out a user"""
    auth.logout(request)
    return redirect("/")


# Called when user enters OTP
def confirm_otp_view(request):

# Create a UserProfile
# Added on 29/07/2024
# get_or_create returns tuple
# created is a boolean , True if model bject is created
# False if model object is fetched
# user_profile is a model object created or fetched
     
     if request.method == 'POST':
         user = request.session['user']
         print('User: ',user)
         generated_otp = request.session['generated_otp']
         # Get OTP
         otp = request.POST['otp']
         # Compare with generated OTP
         #otp_form = AuthenticationForm(request.POST or None)
         if (generated_otp == otp):

            new_user = CustomUser.objects.get(username=user)
            user_type = new_user.user_type
            print("In confirm_otp_view, User type: ", user_type)
            if (user_type == 'buyer'):
                # Buyer registration
                new_user.user_type=new_user.BUYER # Buyer
                new_user.user_type = user_type
                new_user.approve_user()
                new_user.save()
                # Create Buyer
                # VBhat 28-06-2025

                buyer, created = Buyer.objects.get_or_create(
                        user=new_user,is_deleted='N')    
                #buyer.user_type =new_user.SELLER # Seller           
                buyer.approve_buyer()
                buyer.save()
                
                #password = request.session['password']
                password = request.session['password']
                # Send email / SMS to be called
                # Send user account details     
                send_user_account_details(new_user,password, new_user.username,new_user.email)
                # Login and display home page
                # For the time being redirect
                return redirect('/buyer_login/')
            else:
                # Seller registration
                new_user.user_type=new_user.SELLER # seller
                new_user.approve_user()
                new_user.save()
                # Create Buyer
                # VBhat 28-06-2025

                seller, created = Seller.objects.get_or_create(
                        user=new_user,is_deleted='N')               
                seller.approve_seller()
                seller.save()
                
                #password = request.session['password']
                password = request.session['password']
                # Send email / SMS to be called
                # Send user account details     
                send_user_account_details(new_user,password, new_user.username,new_user.email)
                # Login and display home page
                # For the time being redirect
                return redirect('/seller_login/')
         else: 
                # Entered OTP is wrong. 
                #request.session['otp_message'] = f'Entered OTP= {otp},  generated_otp= {generated_otp}, Please try again.'
                request.session['otp_message'] = f'Entered OTP is wrong, Please try again.'
                request.session['retry_otp'] = 'yes'
                generate_and_send_otp(request)
                return(display_otp_page(request))
     
def generate_and_send_otp(request):
     # Generate OTP
     otp = randint(100000, 999999)

     request.session['generated_otp']= str(otp)
     user_name = request.session['user']
    
     # Send OTP
     to_email = request.session['email']
     send_otp_email(otp, user_name, to_email)

# Function to compose and send user registration details
# Called after registration
def send_user_account_details_original(user,password, user_name,to_email_address):
    # Compose and send an email
    subject = "Online Quiz/Test - Your login details"
    body = f'''Dear user\n Your login details are as follows:.\n\n 
            Your login user name: {user_name}\n\n 
            password: {password}\n\n
            Your Name: {user.first_name}
            
            Your registered contact number: {user.contact_number}\n\n
            Your registered email address: {to_email_address}\n\n
            Your address: {user.postal_address}\n\n
            District: {user.district}\n\n
            State: {user.state}\n\n
            Country: {user.country}
            Postal code: {user.pin_code}
            \nUse the following to read Online quiz instructions:https://www.krishnacontest.vbquest.com/instructions/
            \nTo complete the registration, please pay registration fees
            \n\nUse the following link login and select a quiz to make payment https://www.krishnacontest.vbquest.com/index/
            \n
            '''
    email_msg = f"Subject: {subject}\n\n{body}"
    send_email(email_msg,to_email_address)

# Function to compose and send user registration details
# Called after registration
def send_user_account_details(user,password, user_name,to_email_address):
    # Compose and send an email
    subject = "Flower Market.com - Your login details"
    body = f'''Dear user\n Your login details are as follows:.\n\n 
            Your login user name: {user_name}\n\n 
            password: {password}\n\n
            Your Name: {user.first_name}
            
            Your registered contact number: {user.contact_number}\n\n
            Your registered email address: {to_email_address}\n\n            
            '''
    email_msg = f"Subject: {subject}\n\n{body}"
    send_email(email_msg,to_email_address)

# Function to send OTP
# called when an new user registers (Create user account)

def send_otp_email(otp, user_name, to_email):
    #  Compose email
    subject = "OTP"
    body = f"Dear user\n Your OTP.\n\n  {otp}\n\n "
    email_subject_body = f"Subject: {subject}\n\n{body}"

# Send the Email
    send_email(email_subject_body,to_email)

# For sending an email with image file attachment
def send_email_with_image(to_email_address, email_subject, email_body, image_path):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from django.conf import settings

    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    # Set up the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email_address
    message['Subject'] = email_subject

    # Attach the email body
    message.attach(MIMEText(email_body, 'plain'))

    # Attach the image file
    try:
        with open(image_path, 'rb') as img_file:
            mime_base = MIMEBase('image', 'jpeg')  # Change 'jpeg' to the appropriate type (e.g., 'png', 'gif')
            mime_base.set_payload(img_file.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename={image_path.split("/")[-1]}')
        message.attach(mime_base)
    except FileNotFoundError:
        print("Image file not found. Please check the file path.")
        return

    # Create SMTP session and send the email
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email_address, message.as_string())
    server.quit()

# Called from send_otp_email, send_forgot_password, send_password
# VBhat 03-12-2024

def send_email(email_subject_body, to_email_address):
   

    import smtplib
    from email.mime.text import MIMEText

    # Configuration
    
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    
    sender_password = settings.EMAIL_HOST_PASSWORD  # Your password generated by Mailtrap

    sender_email = settings.EMAIL_HOST_USER
    #sender_email = "vishwagitaforum@gmail.com"

    server = smtplib.SMTP(smtp_server,port)

    # Create SMTP Session
    server.starttls()

    # Login to the Server
    server.login(sender_email,sender_password)

    # Send an Email
    try:
        server.sendmail(sender_email, to_email_address, email_subject_body)
    except:
         error_msg = f"<h1>Server Error Contact: {sender_email} </h1>"
         return HttpResponse(error_msg)

# Called when a user selects Forgot password option

def send_forgot_password_email(new_password, user_name, to_email_address):   
      
    # Compose an Email  
 
    subject = "Password has been reset"
    body = f"Dear user\n Your password has been reset.\n\n Your login user name: {user_name}\n\n New password: {new_password}"
    email_msg = f"Subject: {subject}\n\n{body}"
    new_password = new_password  # Your login generated by Mailtrap
    send_email(email_msg,to_email_address)



def shipping_address_view(request):
    #return HttpResponse("Buyer's Shipping Address")
    return render(request,"accounts/buyer_shipping_address.html")

def buyer_view(request):
    #return HttpResponse("Buyer's Page")
    return render(request,"accounts/buyer.html")

def buyer_change_password_view(request):
    return render(request,"accounts/buyer_change_password.html")
    #return HttpResponse("Buyer's Change Password Page")


