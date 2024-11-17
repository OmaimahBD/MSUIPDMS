
from django.shortcuts import  render, redirect ,HttpResponse
from .models import IntellectualProperty, College, Comment, CommenReply, Type, User,Student, Department,SubType
from .forms import  IntellectualPropertyForm,  StudentForm, UserForm,UpdatePasswordForm
from django.db.models import Q # use this for dynamic searching
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.dateparse import parse_date


def home(request):
     context={     }
     
     return render(request,'home.html',context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
   
  
    context = {'user': user}
    return render(request, 'profile.html', context)


def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'UpdateUser.html', {'form': form})

def UpdatePassword(request):

    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form = UpdatePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password Updated please log in again')
                return redirect('LoginView')
        else:
            form = UpdatePasswordForm(user)

    else:
        messages.error(request,'you must be logged in')


 
    return render(request, 'UpdatePassword.html', {'form': form})





def UploadedIP(request):
 
    if not request.user.is_authenticated:
       
        return redirect('LoginView')  


    IP = IntellectualProperty.objects.filter(
        Q(host=request.user) | Q(author=request.user)  | Q(mainauthor=request.user) 
    ).distinct()
    
   
    
 
    context = {
        'IP': IP,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'UploadedIP.html', context)


def room(request):
    query = request.GET.get('q', '')  
    search_performed = False
 
    IP = IntellectualProperty.objects.all()
    IP_count = IP.count()

    if query:
        
        IP = IntellectualProperty.objects.filter(
            Q(type__type__icontains=query) |
            Q(college__name__icontains=query) |
            Q(description__icontains=query) |
            Q(tittle__icontains=query) |
            Q(author__username__icontains=query),
            is_approved = True
        
        )
        search_performed = True
    else:
        IP = IntellectualProperty.objects.all()
        search_performed = False
   
    topics = College.objects.all()
    types = Type.objects.all()

    context = {
        'IP': IP,
        'topics': topics,
        'types': types,
        'IP_count': IP_count,
        'search_performed': search_performed,
        'query': query,
    }
    return render(request, 'room.html', context)



def LoginView(request):
   
   page = 'login'
   errormessage=''
   if request.method == 'POST':
        username = request.POST['email'].lower()
        password = request.POST['Password']
     
       
        try:
           user = User.objects.get(username=username)
          
        except:
           errormessage = 'User does not exist'
           return render(request,'login_reg.html',{'page':page,'errormessage': errormessage})

        user = authenticate(request, username=username , password=password) 
        
        if user is not None and user.is_superuser :
            login(request, user)
            return redirect('AdminHome')
        elif user is not None and user.is_coordinator and user.is_activated:
            login(request, user)
            return redirect('AdminHome')
        elif user is not None and user.is_student and user.is_activated:
            login(request, user)
            return redirect('home')
        
        
        else:
            errormessage = 'Username or password does not exist'
            return render(request,'login_reg.html',{'page':page,'errormessage': errormessage})
          
     
   print(errormessage)

   context={'page': page, 'errormessage': errormessage}
   
   return render(request,'login_reg.html',context)



def RegisterView(request):
   
    form = StudentForm()
    errormessage =''
    successmessage =''
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user is not None:
                user.username = user.username.lower()   
                user.is_student = True          
                user.save()
                student = Student.objects.create(user=user)
                student.save()
                successmessage='You successfully submit your registration, admin/coordinator will validate your account. Please check your email'
                form = StudentForm()
                return render(request,'login_reg.html',{ 'form': form,'successmessage': successmessage})
            else:
                errormessage='form invalid'
        else:
            error_messages = [f" {', '.join(errors)}" for field, errors in form.errors.items()]
            errormessage = '' + ' '.join(error_messages)
    print(successmessage)  
    print(errormessage) 
    

    return render(request,'login_reg.html',{'form': form, 'errormessage':errormessage, 'successmessage': successmessage})




def LogoutView(request):
    logout(request)
    return redirect('home')






def intellectualProperty(request, pk):
    IP = IntellectualProperty.objects.get(id=pk)
    IP.ipviews += 1
    print(IP.ipviews)
    IP.save()
    open
 
    comments = IP.comment_set.all().order_by('created')

    if request.method == 'POST':
        if 'content' in request.POST:
            Comment.objects.create(
                user=request.user,
                intellectualproperty=IP,
                content=request.POST.get('content')
            )
            return redirect('IntellectualProperty', pk=IP.id)
        elif 'reply_content' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            CommenReply.objects.create(
                user=request.user,
                comment=comment,
                content=request.POST.get('reply_content')
            )
            return redirect('IntellectualProperty', pk=IP.id)

    context = {
        'IP': IP,
        'comments': comments,
    }
    return render(request, 'IntellectualProperty.html', context)


 
def get_user_by_name(last_name, first_name):
    users = User.objects.filter(last_name__iexact=last_name, first_name__iexact=first_name)
    if users.exists():
        return users.first()
    return None

def AddIntellectualProperty(request, pk):
    iptitle = ''
    errormessage = ''
    if request.method == 'POST':
        form = IntellectualPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            IP = form.save(commit=False)
            user = User.objects.get(id=pk)

            college_name = user.college
            try:
                IP.college = College.objects.get(name=college_name)
            except College.DoesNotExist:
                form.add_error('college', f'College "{college_name}" does not exist.')
                return render(request, 'AddIntellectualPropertyForm.html', {'form': form})

            IP.department = user.department
            IP.host = request.user

            
            mainauthor_name = form.cleaned_data.get('mainauthor_username', '').strip()
            if mainauthor_name:
                try:
                    last_name, first_name = mainauthor_name.split(' ', 1)
                    mainauthor = get_user_by_name(last_name, first_name)
                    if mainauthor:
                        IP.mainauthor = mainauthor
                    else:
                       
                        return render(request, 'AddIntellectualPropertyForm.html', {'form': form})
                except ValueError:
                   
                    return render(request, 'AddIntellectualPropertyForm.html', {'form': form})

            
            coauthor_names = [name.strip() for name in form.cleaned_data.get('author', '').split(',') if name.strip()]
            coauthors = []
            for name in coauthor_names:
                try:
                    last_name, first_name = name.split(' ', 1)
                    user = get_user_by_name(last_name, first_name)
                    if user:
                        coauthors.append(user)
                    else:
                        
                        return render(request, 'AddIntellectualPropertyForm.html', {'form': form})
                except ValueError:
                   
                    return render(request, 'AddIntellectualPropertyForm.html', {'form': form})

            
            file = form.cleaned_data.get('file')
            if file:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT / 'ResearchFile')
                filename = fs.save(file.name, file)
                IP.file = fs.url(filename)

            
            request.session['form_data'] = {
                'tittle': form.cleaned_data.get('tittle'),
                'file': file.name if file else None,
                'mainauthor_id': IP.mainauthor.id if IP.mainauthor else None,
                'coauthors_ids': [user.id for user in coauthors],
                'description': form.cleaned_data.get('description'),
                'college': IP.college.name,
                'department': IP.department.name,
                'type_id': form.cleaned_data.get('type').id if form.cleaned_data.get('type') else None,
                'subtype_id': form.cleaned_data.get('subtype').id if form.cleaned_data.get('subtype') else None,
                'year': form.cleaned_data.get('year').strftime('%Y-%m-%d') if form.cleaned_data.get('year') else None,
            }
            return redirect('preview')
        else:
            errormessage = 'Form validation failed. Please correct errors and try again.'
    else:
        form = IntellectualPropertyForm()

    context = {'form': form, 'errormessage': errormessage, 'iptitle': iptitle}
    return render(request, 'AddIntellectualPropertyForm.html', context)


def preview(request):
    form_data = request.session.get('form_data')
    if not form_data:
        messages.error(request, "No data to preview.")
        return redirect('AddIntellectualProperty')

    mainauthor = User.objects.get(id=form_data['mainauthor_id']) if form_data.get('mainauthor_id') else None
    college_instance = College.objects.get(name=form_data['college'])
    department_instance = Department.objects.get(name=form_data['department'])
    type_instance = Type.objects.get(id=form_data['type_id']) if form_data.get('type_id') else None
    subtype_instance = SubType.objects.get(id=form_data['subtype_id']) if form_data.get('subtype_id') else None
    year = parse_date(form_data['year']) if form_data.get('year') else None

    if request.method == 'POST':
        IPupload = IntellectualProperty.objects.create(
            host=request.user,
            tittle=form_data['tittle'],
            mainauthor=mainauthor,
            description=form_data['description'],
            college=college_instance,
            department=department_instance,
            type=type_instance,
            subtype=subtype_instance,
            year=year,
            file=form_data['file'],
        )
        IPupload.author.set(form_data['coauthors_ids'])

        del request.session['form_data']
        messages.success(request, "Intellectual Property uploaded successfully.")
        return redirect('UploadedIP')

    coauthors = User.objects.filter(id__in=form_data['coauthors_ids'])
    file_url = f"{settings.MEDIA_URL}ResearchFile/{form_data['file']}" if form_data.get('file') else None

    return render(request, 'preview.html', {
        'form_data': form_data,
        'mainauthor_name': mainauthor.get_full_name() if mainauthor else "No main author",
        'coauthors': coauthors,
        'type_instance': type_instance,
        'subtype_instance': subtype_instance,
        'year': year,
        'file_url': file_url,
    })


    
def load_department(request):
    college_id = request.GET.get('college_id')
    departments = Department.objects.filter(college_id=college_id).all()

    type_id = request.GET.get('type_id')
    subtypes = SubType.objects.filter(type_id=type_id).all()

    context = {'departments': departments,
            'subtypes' : subtypes  }
    return render(request, 'department_dropdown_list_options.html',context)
 


def UpdateIntellectualProperty(request, pk):

    IP = IntellectualProperty.objects.get(id=pk)
    form = IntellectualPropertyForm(instance=IP)

    if request.user != IP.host:
        return HttpResponse("You are not allowed to update")


    if request.method == 'POST':
        form = IntellectualPropertyForm(request.POST, instance=IP)
        if form.is_valid():
            form.save()
            return redirect('room')
            #return redirect('home')

    context={ 'form': form}
    return render(request,'AddIntellectualPropertyForm.html',context)



def DeleteIntellectualProperty(request, pk):

    IP = IntellectualProperty.objects.get(id=pk)
    if request.user != IP.host:
        return HttpResponse("You are not allowed to delete")
    
    if request.method == 'POST':
        IP.delete()
        return redirect('UploadedIP')
    
    context={ 'obj': IP}
    return render(request,'delete.html',context)

def DeleteComment(request, pk):
    
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse("You are not allowed to delete this comment.")
    
    if request.method == 'POST':
        
        comment.delete()
        return redirect('IntellectualProperty', pk=comment.intellectualproperty.id)
    
    context = {'obj': comment}
    return render(request, 'delete.html', context)

@login_required
def DeleteReply(request, pk):
    reply = CommenReply.objects.get(id=pk)
    if request.user != reply.user:
        return HttpResponse("You are not allowed to delete this reply.")
    
    if request.method == 'POST':
        reply.delete()
        return redirect('IntellectualProperty', pk=reply.comment.intellectualproperty.id)
    
    context = {'obj': reply}
    return render(request, 'delete.html', context)



def CollegePage(request):

    topics = College.objects.filter()

    context ={
        'topics' : topics
    }
    return render(request,'CollegePage.html',context)