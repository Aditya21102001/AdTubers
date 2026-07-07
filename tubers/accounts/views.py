"""Views for the ``accounts`` app — custom auth and the user dashboard.

These are hand-rolled username/password views (not allauth's default pages).
django-allauth is still wired up separately for optional Google/Facebook social
login; see ``tubers/urls.py`` and ``settings.py``.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from contactinfo.models import Contactinfo
from hiretubers.models import Hiretuber


def login(request):
    """Show the login form (GET) or authenticate the submitted credentials (POST)."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate() returns the User on success, or None on bad credentials.
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.warning(request, 'You are logged in.')
            return redirect('dashboard')

        else:
            messages.warning(request, 'Incorrect Credentials')
            return redirect('login')

    contactinfo = Contactinfo.objects.last()
    data = {
        'contactinfo': contactinfo
    }
    return render(request, 'accounts/login.html', data)


def logout_user(request):
    """Log the current user out and return to the homepage."""
    logout(request)
    return redirect('home')


def register(request):
    """Show the sign-up form (GET) or create a new user account (POST)."""
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # Validate: passwords match, and username/email aren't already taken.
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email already exists')
                    return redirect('register')
                else:
                    # create_user() hashes the password before saving.
                    user = User.objects.create_user( first_name = firstname, last_name = lastname, username = username, email = email, password = password )
                    user.save()
                    messages.success(request, 'Account created Successfully')
                    return redirect('login')

        else:
            messages.warning(request, 'Password do not match')
            return redirect('register')
    contactinfo = Contactinfo.objects.last()
    data = {
        'contactinfo': contactinfo
    }
    return render(request, 'accounts/register.html', data)


@login_required(login_url='login')
def dashboard(request):
    """Logged-in user's dashboard: lists the booking requests they submitted."""
    # Bookings are matched by user_id (a plain integer field, not a FK).
    bookings = Hiretuber.objects.filter(user_id=request.user.id).order_by('-created_date')
    contactinfo = Contactinfo.objects.last()
    data = {
        'contactinfo': contactinfo,
        'bookings': bookings,
    }
    return render(request, 'accounts/dashboard.html', data)
