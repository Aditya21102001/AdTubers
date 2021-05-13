from django.shortcuts import get_object_or_404, render
from .models import Youtuber
from  contactinfo.models import Contactinfo

def youtubers(request):
    contactinfo = Contactinfo.objects.latest('id')
    tubers = Youtuber.objects.order_by('-created_date')
    city = Youtuber.objects.values_list('city', flat=True).distinct()
    camera_type = Youtuber.objects.values_list('camera_type', flat=True).distinct()
    category = Youtuber.objects.values_list('category', flat=True).distinct()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            tubers=tubers.filter(description__icontains=keyword)
    
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            tubers=tubers.filter(city__iexact=city)

    if 'camera_type' in request.GET:
        camera_type = request.GET['camera_type']
        if camera_type:
            tubers=tubers.filter(camera_type__iexact=camera_type)

    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            tubers=tubers.filter(category__iexact=category)

    data={
        'contactinfo':contactinfo,
        'tubers':tubers,
        'city':city,
        'camera_type':camera_type,
        'category':category
    }
    return render(request, 'youtubers/youtubers.html', data)

def youtubers_detail(request, id):
    contactinfo = Contactinfo.objects.latest('id')
    tuber = get_object_or_404(Youtuber, pk=id)
    data={
        'contactinfo':contactinfo ,
        'tuber' : tuber
    }
    return render(request, 'youtubers/youtuber_detail.html', data)
    


def search(request):
    contactinfo = Contactinfo.objects.latest('id')
    tubers = Youtuber.objects.order_by('-created_date')
    city = Youtuber.objects.values_list('city', flat=True).distinct()
    camera_type = Youtuber.objects.values_list('camera_type', flat=True).distinct()
    category = Youtuber.objects.values_list('category', flat=True).distinct()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            tubers=tubers.filter(description__icontains=keyword)
    
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            tubers=tubers.filter(city__iexact=city)

    if 'camera_type' in request.GET:
        camera_type = request.GET['camera_type']
        if camera_type:
            tubers=tubers.filter(camera_type__iexact=camera_type)

    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            tubers=tubers.filter(category__iexact=category)

    data={
        'contactinfo':contactinfo,
        'tubers':tubers,
        'city':city,
        'camera_type':camera_type,
        'category':category
        

    }
    return render(request, 'youtubers/search.html', data)

# Create your views here.
