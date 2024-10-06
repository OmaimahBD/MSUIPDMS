from django.shortcuts import  render, redirect ,HttpResponse
from .models import IntellectualProperty, College, Comment, CommenReply, Type, User,Student, Department,SubType
from .forms import  IntellectualPropertyForm,  StudentForm, UserForm,UpdatePasswordForm
from django.db.models import Q # use this for dynamic searching
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
       
        return redirect('login')  


    IP = IntellectualProperty.objects.filter(
        Q(host=request.user) | Q(author=request.user)  | Q(mainauthor=request.user) 
    ).distinct()
    
   
    
 
    context = {
        'IP': IP,
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
    iptitle=''
    errormessage=''
    if request.method == 'POST':
        form = IntellectualPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            IP = form.save(commit=False)
            user = User.objects.get(id=pk)
            IP.college = user.college
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
                        form.add_error('mainauthor_username', f'Main author with name "{mainauthor_name}" does not exist.')
                        error_messages = [f" {', '.join(errors)}" for field, errors in form.errors.items()]
                        errormessage = '' + ' '.join(error_messages)
                        return render(request, 'AddIntellectualPropertyForm.html', {'form': form,'errormessage':errormessage})
                except ValueError:
                    form.add_error('mainauthor_username', 'Main Author: Please enter the name in "lastname firstname" format.')
                    error_messages = [f" {', '.join(errors)}" for field, errors in form.errors.items()]
                    errormessage = '' + ' '.join(error_messages)
                    return render(request, 'AddIntellectualPropertyForm.html', {'form': form,'errormessage':errormessage})
            else:
                IP.mainauthor = None
        
      
           

            author_names = form.cleaned_data.get('author', '')
            coauthor_names = [name.strip() for name in author_names.split(',') if name.strip()]

            users = []
            user_does_not_exist = False
            for name in coauthor_names:
                try:
                    last_name, first_name = name.split(' ', 1)
                    user = get_user_by_name(last_name, first_name)
                    if user:
                        users.append(user)
                    else:
                        form.add_error('author', f'Co-author with name "{name}" does not exist.')
                        user_does_not_exist = True
                        error_messages = [f" {', '.join(errors)}" for field, errors in form.errors.items()]
                        errormessage = '' + ' '.join(error_messages)
                        return render(request, 'AddIntellectualPropertyForm.html', {'form': form,'errormessage':errormessage})
                except ValueError:
                    form.add_error('author', f'Co-authors: Invalid name format "{name}". Use "lastname firstname, lastname firstname".')
                    user_does_not_exist = True
                    error_messages = [f" {', '.join(errors)}" for field, errors in form.errors.items()]
                    errormessage = '' + ' '.join(error_messages)
                    return render(request, 'AddIntellectualPropertyForm.html', {'form': form,'errormessage':errormessage})

            if user_does_not_exist:
                users = [request.user]
           

            request.session['form_data'] = {
                'tittle': form.cleaned_data.get('tittle'), 
                'file': form.cleaned_data.get('file').name if form.cleaned_data.get('file') else None,
                'mainauthor_id': mainauthor.id if mainauthor else None,
                'coauthors_ids': [user.id for user in users],
            }
    
            return redirect('preview')
        else:
            errormessage = 'Intellectual Property with the same title exist' 
            return render(request, 'AddIntellectualPropertyForm.html', {'form': form,'errormessage':errormessage})  
           
    else:
        form = IntellectualPropertyForm()  
         

    context = {'form': form, 'errormessage':errormessage, 'iptitle':iptitle}
    return render(request, 'AddIntellectualPropertyForm.html', context)

def preview(request):
    form_data = request.session.get('form_data')
     
    mainauthor_id = form_data.get('mainauthor_id')
    mainauthor = User.objects.get(id=mainauthor_id) if mainauthor_id else None
    if request.method == 'POST':
        
        IPupload = IntellectualProperty.objects.create(
            host=request.user,
            tittle=form_data.get('tittle'),
            file=form_data.get('file'), 
            mainauthor=mainauthor,
        )
        
       
        coauthors_ids = form_data.get('coauthors_ids', [])
        IPupload.author.set(coauthors_ids) 
     
        del request.session['form_data']  
        return redirect('UploadedIP') 
    
    mainauthor_name = mainauthor.get_full_name() if mainauthor else "No main author"
    coauthors = User.objects.filter(id__in=form_data.get('coauthors_ids', []))

    return render(request, 'preview.html', {'form_data': form_data, 'mainauthor_name':mainauthor_name, 'coauthors':coauthors})

    
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
    # return redirect('home')
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