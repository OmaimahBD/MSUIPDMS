from django.shortcuts import  render, redirect
from core.models import IntellectualProperty, College, Comment, Type, User,Student
from django.db.models import Q 

def IPDMS(request):
     
    context={}
    return render(request,'IPDMS.html',context)

def vision(request):
     
    context={}
    return render(request,'vision.html',context)

def mission(request):
     
    context={}
    return render(request,'mission.html',context)

def goals(request):
     
    context={}
    return render(request,'goals.html',context)

def objectives(request):
     
    context={}
    return render(request,'objectives.html',context)

def copyright(request):
     
    context={}
    return render(request,'copyright.html',context)

def patent(request):
     
    context={}
    return render(request,'patent.html',context)

def trademark(request):
     
    context={}
    return render(request,'trademark.html',context)
def about(request):
     
    context={}
    return render(request,'about.html',context)
def admincoorabout(request):
     
    context={}
    return render(request,'AdminCoor/about.html',context)
def policy(request):
     
    context={}
    return render(request,'policy.html',context)

def admincoorpolicy(request):
     
    context={}
    return render(request,'AdminCoor/policy.html',context)



def admincoorroom(request):
     #IP = IntellectualProperty.objects.all()
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    IP = IntellectualProperty.objects.all()
    IP_count = IP.count()
    IP = IntellectualProperty.objects.filter(
        Q(type__type__icontains=query) |
         Q(college__name__icontains=query) |
        Q(description__icontains=query) |
        Q(tittle__icontains=query) |
        Q(author__icontains=query)
      
    )[0:2]
   
   
    topics = College.objects.all()[0:2]
    types = Type.objects.all()
  
    context={
       'IP' : IP,
       'topics' : topics,
       'types' : types,
       'IP_count': IP_count,
       
   }
    return render(request,'AdminCoor/room.html',context)



def admincoorintellectualProperty(request, pk):
   
   IP = IntellectualProperty.objects.get(id=pk)
   comments = IP.comment_set.all().order_by('created')

   if request.method == 'POST':
       comments = Comment.objects.create(
           user = request.user,
           intellectualproperty=IP,
           content=request.POST.get('content')
           )
       return redirect('AdmincoorIntellectualProperty', pk=IP.id)

       
   context={
       'IP' : IP,
       'comments': comments,     
       
   }
   return render (request,'AdminCoor/IntellectualProperty.html',context)


def admincoorIntellectualPropertyPage(request):
     #IP = IntellectualProperty.objects.all()
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    IP = IntellectualProperty.objects.all()
    IP_count = IP.count()
    IP = IntellectualProperty.objects.filter(
        Q(type__type__icontains=query) |
         Q(college__name__icontains=query) |
        Q(description__icontains=query) |
        Q(tittle__icontains=query) |
        Q(author__icontains=query)
      
    )
   
   
    topics = College.objects.all()[0:2]
    types = Type.objects.all()
  
    context={
       'IP' : IP,
       'topics' : topics,
       'types' : types,
       'IP_count': IP_count,
       
   }
    return render(request,'AdminCoor/IntellectualPropertyPage.html',context)



def admincoorroom2(request):
     #IP = IntellectualProperty.objects.all()
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    IP = IntellectualProperty.objects.all()
    IP_count = IP.count()
    IP = IntellectualProperty.objects.filter(
        Q(type__type__icontains=query) |
         Q(college__name__icontains=query) |
        Q(description__icontains=query) |
        Q(tittle__icontains=query) |
        Q(author__icontains=query)
      
    )
   
   
    topics = College.objects.all()
    types = Type.objects.all()
  
    context={
       'IP' : IP,
       'topics' : topics,
       'types' : types,
       'IP_count': IP_count,
       
   }
    return render(request,'AdminCoor/room2.html',context)





