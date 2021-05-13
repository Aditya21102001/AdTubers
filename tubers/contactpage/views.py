from django.shortcuts import render, redirect
from .models import Contactpage
from django.contrib import messages

# Create your views here.
def contactpage(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        subject = request.POST['subject']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        contactpage = Contactpage( first_name=first_name, subject=subject, phone=phone, email=email, message=message )
        contactpage.save()
        messages.success(request, 'Thanks for reaching out!')
        return redirect('youtubers')

