from django.shortcuts import  render, redirect ,HttpResponse
#from django.template import loader
from .models import IntellectualProperty, College, Comment, Type, User
from django.db.models import Q # use this for dynamic searching
from django.db.models import Count
import datetime
from django.db.models import Count, Case, When
#from django.contrib.auth.forms import UserCreationFo
# rm

def NumIPCollege(request):
  
    data = IntellectualProperty.objects.filter(is_approved = True ).values('college__name').annotate(
        patents=Count(Case(When(type__type='Patent', then=1))),
        trademarks=Count(Case(When(type__type='Trademark', then=1))),
        copyrights=Count(Case(When(type__type='Copyright', then=1))),
    ).order_by('college__name')
        
    

    labels = [item['college__name'] for item in data]
    patents = [item['patents'] for item in data]
    trademarks = [item['trademarks'] for item in data]
    copyrights = [item['copyrights'] for item in data]

    context = {
        'labels': labels,
        'patents': patents,
        'trademarks': trademarks,
        'copyrights': copyrights,
    }
    return render(request, 'Charts/NumIpColleges.html', context)

def NumIPCollege1(request):
    data = IntellectualProperty.objects.aggregate(
        patents=Count(Case(When(type__type='Patent', then=1))),
        trademarks=Count(Case(When(type__type='Trademark', then=1))),
        copyrights=Count(Case(When(type__type='Copyright', then=1)))
    )

    labels = ['Patents', 'Trademarks', 'Copyrights']
    values = [data['patents'], data['trademarks'], data['copyrights']]

    context = {
        'labels': labels,
        'values': values,
    }
    return render(request, 'Charts/NumIpColleges1.html', context)

def NumIp(request):
    
    data = IntellectualProperty.objects.values('type__type', 'created__week_day').annotate(count=Count('id')).order_by('created__week_day', 'type__type')
    
   
    patent_data = {day: 0 for day in range(1, 8)}
    copyright_data = {day: 0 for day in range(1, 8)}
    trademark_data = {day: 0 for day in range(1, 8)}
    
   
    for item in data:
        if item['type__type'] == 'Patent':
            patent_data[item['created__week_day']] = item['count']
        elif item['type__type'] == 'Copyright':
            copyright_data[item['created__week_day']] = item['count']
        elif item['type__type'] == 'Trademark':
            trademark_data[item['created__week_day']] = item['count']

    
    data1 = [patent_data[day] for day in range(1, 8)]
    data2 = [copyright_data[day] for day in range(1, 8)]
    data3 = [trademark_data[day] for day in range(1, 8)]

    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request, 'Charts/NumIp.html', context)



def mostviewedip(request):
    top_ips = IntellectualProperty.objects.order_by('-ipviews')[:10]
    ip_titles = [ip.tittle for ip in top_ips]
    ip_views = [ip.ipviews for ip in top_ips]
    ip_links = [f'/intellectual_property/{ip.pk}/' for ip in top_ips]  # Assuming you have a URL pattern for individual IPs

    context = {
        'ip_titles': ip_titles,
        'ip_views': ip_views,
        'ip_links': ip_links
    }
    return render(request, 'Charts/mostviewed.html', context)

