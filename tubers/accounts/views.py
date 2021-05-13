from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from contactinfo.models import Contactinfo
from youtubers.models import Youtuber


# Create your views here.
def login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.warning(request, 'You are logged in.')
            return redirect('dashboard')

        else:
            messages.warning(request, 'Incorrect Credentials')
            return redirect('login')

    contactinfo = Contactinfo.objects.latest('id')
    data = {
        'contactinfo' : contactinfo
    }    
    return render(request, 'accounts/login.html', data)


def logout_user(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.warning(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.warning(request, 'Email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user( first_name = firstname, last_name = lastname, username = username, email = email, password = password )
                    user.save()
                    messages.success(request, 'Account created Successfully')
                    return redirect('login')

        else:
            messages.warning(request, 'Password do not match')
            return redirect('register')
    contactinfo = Contactinfo.objects.latest('id')
    data = {
        'contactinfo' : contactinfo
    }
    return render(request, 'accounts/register.html', data)

@login_required(login_url='login')
def dashboard(request):
    tubers = Youtuber.objects.order_by('-created_date')
    contactinfo = Contactinfo.objects.latest('id')
    data={
        'contactinfo':contactinfo,
        'tubers':tubers
    }
    return render(request, 'accounts/dashboard.html', data)