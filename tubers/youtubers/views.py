from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from contactinfo.models import Contactinfo
from .models import Youtuber
from .recommender import rank_youtubers


def _filter_tubers(request, tubers):
    """Apply the keyword/city/camera/category filters from the GET params."""
    keyword = request.GET.get('keyword')
    if keyword:
        tubers = tubers.filter(description__icontains=keyword)

    city = request.GET.get('city')
    if city:
        tubers = tubers.filter(city__iexact=city)

    camera_type = request.GET.get('camera_type')
    if camera_type:
        tubers = tubers.filter(camera_type__iexact=camera_type)

    category = request.GET.get('category')
    if category:
        tubers = tubers.filter(category__iexact=category)

    return tubers


def _dropdown_options():
    """Distinct values used to populate the search dropdowns."""
    return {
        'city': Youtuber.objects.values_list('city', flat=True).distinct(),
        'camera_type': Youtuber.objects.values_list('camera_type', flat=True).distinct(),
        'category': Youtuber.objects.values_list('category', flat=True).distinct(),
    }


def _paginate(request, queryset, per_page=8):
    """Return (page_obj, base_query); base_query keeps active filters in page links."""
    page_obj = Paginator(queryset, per_page).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    return page_obj, params.urlencode()


def youtubers(request):
    tubers = _filter_tubers(request, Youtuber.objects.order_by('-created_date'))
    page_obj, base_query = _paginate(request, tubers)
    data = {
        'contactinfo': Contactinfo.objects.last(),
        'tubers': page_obj,
        'page_obj': page_obj,
        'base_query': base_query,
    }
    data.update(_dropdown_options())
    return render(request, 'youtubers/youtubers.html', data)


def youtubers_detail(request, id):
    data = {
        'contactinfo': Contactinfo.objects.last(),
        'tuber': get_object_or_404(Youtuber, pk=id),
    }
    return render(request, 'youtubers/youtuber_detail.html', data)


def search(request):
    tubers = _filter_tubers(request, Youtuber.objects.order_by('-created_date'))
    page_obj, base_query = _paginate(request, tubers)
    data = {
        'contactinfo': Contactinfo.objects.last(),
        'tubers': page_obj,
        'page_obj': page_obj,
        'base_query': base_query,
    }
    data.update(_dropdown_options())
    return render(request, 'youtubers/search.html', data)


def recommend(request):
    """AI creator match: rank creators against a free-text event brief."""
    query = request.GET.get('q', '').strip()
    results = rank_youtubers(query, Youtuber.objects.all()) if query else []
    data = {
        'contactinfo': Contactinfo.objects.last(),
        'query': query,
        'results': results,
    }
    return render(request, 'youtubers/recommend.html', data)
