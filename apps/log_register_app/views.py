from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    if 'userid' in request.session:
        return redirect('/books')
    else:
        return render(request, 'index.html')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['logemail'])
        if user: 
            logged_user = user[0]
        else:
            messages.error(request, "Incorrect user or password")
            context = {
                'entered_email': request.POST['logemail']
            }
            return render(request, 'index.html', context)
        if bcrypt.checkpw(request.POST['logpassword'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/books')
        else:
            messages.error(request, "Incorrect user or password")
            context = {
                'entered_email': request.POST['logemail']
            }
            return render(request, 'index.html', context)

def logout(request):
    if request.session['userid']:
        del request.session['userid']
        messages.success(request, "Succesfully logged out")
        return redirect('/')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        errors = User.objects.validations(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {
                'fname': request.POST['fname'],
                'lname': request.POST['lname'],
                'email': request.POST['email'],
                'birthday_date': request.POST['birthday_date']
            }
            return render(request, 'index.html', context)
        else:
            password=request.POST['password']
            pw_hash= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            User.objects.create(
            fname=f"{request.POST['fname']}",
            lname=f"{request.POST['lname']}",
            email=f"{request.POST['email']}", 
            birthday_date=f"{request.POST['birthday_date']}",
            password=pw_hash)
            messages.success(request, "User succesfully created")
            return redirect('/')