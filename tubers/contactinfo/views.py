from django.shortcuts import render, redirect
from .models import Contactinfo
from django.contrib import messages

# Create your views here.
def contactinfo(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        fb_handle = request.POST['fb_handle']
        insta_handle = request.POST['insta_handle']
        youtube_handle = request.POST['youtube_handle']
        twitter_handle = request.POST['twitter_handle']
        phone = request.POST['phone']
        email = request.POST['email']
        contactinfo = Contactinfo( first_name=first_name, last_name=last_name, fb_handle=fb_handle, insta_handle=insta_handle, youtube_handle=youtube_handle, twitter_handle=twitter_handle, phone=phone, email=email )
        contactinfo.save()
        messages.success(request, 'Thanks for reaching out!')
        return redirect('youtubers')
        

