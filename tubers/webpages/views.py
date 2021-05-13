from django.shortcuts import render
from .models import Slider, Team
from youtubers.models import Youtuber
from  contactinfo.models import Contactinfo



# Create your views here.
def home(request):
    featured_youtubers=Youtuber.objects.order_by('-created_date').filter(is_featured=True)
    all_tubers=Youtuber.objects.order_by('-created_date')
    sliders = Slider.objects.all()
    teams = Team.objects.all()
    contactinfo = Contactinfo.objects.latest('id')
    data = {
        'contactinfo' : contactinfo,
        'sliders' : sliders, 
        'teams' : teams,
        'featured_youtubers' : featured_youtubers,
        'all_tubers' : all_tubers
    }
    return render(request, 'webpages/home.html', data)

def about(request):
    teams = Team.objects.all()
    contactinfo = Contactinfo.objects.latest('id')
    data = {
        'contactinfo' : contactinfo,
        'teams' : teams
    }
    return render(request, 'webpages/about.html', data)

def services(request):
    tubers = Youtuber.objects.order_by('-created_date')
    sliders = Slider.objects.all()
    contactinfo = Contactinfo.objects.latest('id')
    data = {'sliders' :sliders,
        'contactinfo' : contactinfo,
        'tubers' : tubers
    }
    return render(request, 'webpages/services.html',data)

def contact(request):
    contactinfo = Contactinfo.objects.latest('id')
    data = {
        'contactinfo' : contactinfo
    }
    return render(request, 'webpages/contact.html', data)