"""View for the ``contactpage`` app — receives public contact-form messages.

POST-only. Saves the submitted message as a :class:`Contactpage` row and
redirects to the creator list with a thank-you flash message.
"""

from django.shortcuts import render, redirect
from .models import Contactpage
from django.contrib import messages


def contactpage(request):
    """Save a submitted contact message, then flash a thank-you and redirect."""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        subject = request.POST['subject']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        contactpage = Contactpage( first_name=first_name, subject=subject, phone=phone, email=email, message=message )
        contactpage.save()
        messages.success(request, 'Thanks for reaching out!')
        # Post/Redirect/Get: redirect so a refresh doesn't resubmit the form.
        return redirect('youtubers')
