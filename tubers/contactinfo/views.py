"""View for the ``contactinfo`` app.

POST-only endpoint that creates a :class:`Contactinfo` row from submitted form
fields. In normal use the site's contact details are managed through the admin;
this view exists for a form-driven create path.
"""

from django.shortcuts import render, redirect
from .models import Contactinfo
from django.contrib import messages


def contactinfo(request):
    """Create a Contactinfo row from posted fields, then flash and redirect."""
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
        # Post/Redirect/Get: redirect so a refresh doesn't resubmit the form.
        return redirect('youtubers')
