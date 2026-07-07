"""Views for the ``webpages`` app — the public marketing pages.

Four read-only pages (home, about, services, contact). Each one loads the data
it needs, always including the single :class:`Contactinfo` row so the shared
header/footer can show the site's contact details.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Slider, Team
from youtubers.models import Youtuber
from contactinfo.models import Contactinfo


def home(request):
    """Landing page: carousel, featured creators, full creator row, and team."""
    featured_youtubers = Youtuber.objects.order_by('-created_date').filter(is_featured=True)
    all_tubers = Youtuber.objects.order_by('-created_date')
    sliders = Slider.objects.all()
    teams = Team.objects.all()
    contactinfo = Contactinfo.objects.last()  # single site-wide contact row
    data = {
        'contactinfo': contactinfo,
        'sliders': sliders,
        'teams': teams,
        'featured_youtubers': featured_youtubers,
        'all_tubers': all_tubers
    }
    return render(request, 'webpages/home.html', data)


def about(request):
    """About Us page: shows the team members."""
    teams = Team.objects.all()
    contactinfo = Contactinfo.objects.last()
    data = {
        'contactinfo': contactinfo,
        'teams': teams
    }
    return render(request, 'webpages/about.html', data)


def services(request):
    """Services page: lists creators (paginated) alongside the banner sliders."""
    tubers = Youtuber.objects.order_by('-created_date')
    sliders = Slider.objects.all()
    contactinfo = Contactinfo.objects.last()
    # Paginate to 8 per page and carry any other GET params in the page links.
    page_obj = Paginator(tubers, 8).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    data = {
        'sliders': sliders,
        'contactinfo': contactinfo,
        'tubers': page_obj,
        'page_obj': page_obj,
        'base_query': params.urlencode(),
        # Distinct values that populate the search dropdowns (form posts to search).
        'city': Youtuber.objects.values_list('city', flat=True).distinct(),
        'camera_type': Youtuber.objects.values_list('camera_type', flat=True).distinct(),
        'category': Youtuber.objects.values_list('category', flat=True).distinct(),
    }
    return render(request, 'webpages/services.html', data)


def contact(request):
    """Contact page: the contact details / form. (Form posts to the contactpage app.)"""
    contactinfo = Contactinfo.objects.last()
    data = {
        'contactinfo': contactinfo
    }
    return render(request, 'webpages/contact.html', data)
