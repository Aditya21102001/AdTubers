"""View for the ``hiretubers`` app — receives booking requests.

A single POST-only endpoint. The form lives on the creator detail page
(``templates/youtubers/youtuber_detail.html``); this view saves the submitted
fields as a :class:`Hiretuber` row and redirects back to the creator list.
"""

from django.shortcuts import render, redirect
from .models import Hiretuber
from django.contrib import messages


def hiretuber(request):
    """Save a submitted booking request, then flash a thank-you and redirect."""
    if request.method == 'POST':
        # Pull each field straight from the posted form.
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        tuber_id = request.POST['tuber_id']
        tuber_name = request.POST['tuber_name']
        city = request.POST['city']
        phone = request.POST['phone']
        email = request.POST['email']
        state = request.POST['state']
        message = request.POST['message']
        user_id = request.POST['user_id']  # real user id if logged in, else "00"
        hiretuber = Hiretuber( first_name=first_name, last_name=last_name, tuber_id=tuber_id, tuber_name=tuber_name, city=city, phone=phone, email=email, state=state, message=message, user_id=user_id )
        hiretuber.save()
        messages.success(request, 'Thanks for reaching out!')
        # Post/Redirect/Get: redirect so a refresh doesn't resubmit the form.
        return redirect('youtubers')
