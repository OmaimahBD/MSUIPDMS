from django.shortcuts import  render, redirect
from core.models import User , Coordinator,IntellectualProperty,Department,Comment,Type,SubType
from .forms import  CoordinatorForm, UserForm, AddStudentForm, IntellectualPropertyForm, Student, UpdatePasswordForm, StudentForm, AdminIntellectualPropertyForm
from django.views.generic import CreateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from core.helpers.doc import calc_doc_similarity, preprocess_doc_tokens
import json
from django.utils import timezone
import time
from django.db.models import Count, Case, When
from django.db.models import Q 



def home(request):
    
    types = Type.objects.all()
    users_count = User.objects.filter(is_student=True).count()
    users =User.objects.all().values()

    IP = IntellectualProperty.objects.all()
    approvedIP = [ ip for ip in IP if ip.is_approved==True]

    data = IntellectualProperty.objects.aggregate(
        patents=Count(Case(When(type__type='Patent', then=1))),
        trademarks=Count(Case(When(type__type='Trademark', then=1))),
        copyrights=Count(Case(When(type__type='Copyright', then=1)))
    )
    
    # Get the total counts directly from the data dictionary
    total_patents = data['patents']
    total_trademarks = data['trademarks']
    total_copyrights = data['copyrights']
   
     
    
    filtered_IP = IntellectualProperty.objects.filter(type__type='Patent')
    for i in filtered_IP:
        print(i)
    



   
    top_ips = IntellectualProperty.objects.order_by('-ipviews')[:10]
    ip_titles = [ip.tittle for ip in top_ips]
    ip_views = [ip.ipviews for ip in top_ips]
    ip_links = [f'/intellectual_property/{ip.pk}/' for ip in top_ips]  # Assuming you have a URL pattern for individual IPs

  
   
    context={   
        'total_patents': total_patents,
        'total_trademarks' : total_trademarks,
        'total_copyrights':total_copyrights,
        'users_count':users_count,
        'users': users,      
        'approvedIP': approvedIP,
        'types':types,
        
        'ip_titles': ip_titles,
        'ip_views': ip_views,
        'ip_links': ip_links
      }
   
    return render(request,'AdminCoor/home.html',context)
    


def AdminProfile(request, pk):
    user = User.objects.get(id=pk)
  
    context = {'user': user}
    return render(request, 'AdminCoor/profile.html', context)


def AdminUpdateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Adminprofile', pk=user.id)

    return render(request, 'AdminCoor/UpdateUser.html', {'form': form})


def AdminUpdatePassword(request):

    if request.user.is_superuser or request.user.is_coordinator:
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

    context = {'form': form}
    return render(request, 'AdminCoor/UpdatePassword.html', context)


    
class addCoordinatorOrg(CreateView):
    model = User
    form_class = CoordinatorForm
    template_name = 'Admin/addCoor.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'coordinator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        
        return redirect('AdminCoorHome')
    



def addCoordinator(request):
    
 
    form = StudentForm()

    if request.method == 'POST':
        form = CoordinatorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user is not None:
                user.username = user.username.lower()
                user.is_coordinator = True
                user.is_authenticated = True
                user.is_activated = True
                user.save()
                coordinator = Coordinator.objects.create(user=user)
                coordinator.save()
                
                return redirect('AdminList')
        else: 
            form = StudentForm()

    return render(request, 'AdminCoor/addCoor.html', {'form': form})


def viewCoordinator(request):
  coordinators = User.objects.filter(is_coordinator=True).select_related('college')
  context = {
    'coordinators': coordinators, 
    
  }
  return render(request,'AdminCoor/viewCoor.html',context)

def deleteCoordinator(request, pk):

    user = User.objects.get(id=pk)
    
    
    if request.method == 'POST':
        user.delete()
        return redirect('AdminHome')
    
    context={ 'obj': user}
    return render(request,'AdminCoor/deleteCoor.html',context)


def editCoordinator(request, pk):

    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

   

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('AdminHome')
            #return redirect('home')

    context={ 'form': form}
    return render(request,'AdminCoor/editCoor.html',context)




class addStudentOrg(CreateView):
    model = User
    form_class = StudentForm
    template_name = 'Admin/addStud.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
       
        return redirect('AdminCoorHome')
    




def addStudent(request, pk):
   
    if request.user.is_superuser:
       form = StudentForm()
    elif request.user.is_coordinator:
       form = AddStudentForm()

    if request.method == 'POST':
         
        
        if request.user.is_superuser:
           form = StudentForm(request.POST)
        elif request.user.is_coordinator:
           form = AddStudentForm(request.POST)

        if form.is_valid():
           user = form.save(commit=False)
           if user is not None:
              user.is_student = True
              user.is_authenticated = True
              user.is_activated = True
              if request.user.is_coordinator:
                    user_college = User.objects.get(id=pk)
                    user.college=user_college.college
                    user.department=user_college.department
                    
                   
              user.save()
              student = Student.objects.create(user=user)
              student.save()

              return redirect('AdminStudList')
        else:
             if request.user.is_superuser:
                form = StudentForm()
             elif request.user.is_coordinator:
                form = AddStudentForm()
    else:
            messages.error(request, 'An error occurred during registration')
            print(form.errors)

    return render(request, 'AdminCoor/addStud.html', {'form': form})


    

    

def viewStudent(request):
 
  user_college = request.user.college

  if request.user.is_coordinator:
    users = User.objects.filter(college=user_college)
    approvedStud = [ u for u in users if u.is_authenticated==True]
  elif request.user.is_superuser:
    users = User.objects.all()
    approvedStud = [ u for u in users if u.is_authenticated==True]
      
  context = {
    'approvedStud': approvedStud, 
  }
  return render(request,'AdminCoor/viewStud.html',context)



def deleteStudent(request, pk):

    user = User.objects.get(id=pk)
    
    if request.method == 'POST':
        user.delete()
        return redirect('AdminHome')
    
    context={ 'obj': user}
    return render(request,'AdminCoor/deleteStud.html',context)


def editStudent(request, pk):

    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

   

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('AdminHome')
            

    context={ 'form': form}
    return render(request,'AdminCoor/editStud.html',context)


def ManageStudentRequest(request):

    if request.user.is_coordinator:
        user_college = request.user.college
        users = User.objects.filter(is_authenticated = False, college=user_college)
    elif request.user.is_superuser:
        users = User.objects.filter(is_authenticated = False)

    context={'users': users }
    return render(request,'AdminCoor/manageStudReq.html',context)


def approveStudent(request,pk):

    user = User.objects.get(id=pk) 
    user.is_authenticated = True
    user.is_activated = True
    user.save()
    frommail = settings.EMAIL_HOST_USER
    receiver = [user.email]
    subject = "Registration"
    message = "Congratulations you can now login with MSU IPDMS!"
    send_mail(subject, message, frommail , receiver)         

    return redirect('AdminStudList')


def disapproveStudent(request,pk):

    user = User.objects.get(id=pk) 
    user.is_authenticated = False
    user.save()
    return redirect('AdminStudList')

def activateStudent(request,pk):

    user = User.objects.get(id=pk) 
    if user.is_coordinator:
        user.is_activated = True
        user.save()
        return redirect('AdminList')
    elif user.is_student:
        user.is_activated = True
        user.save()
        return redirect('AdminStudList')

def deactivateStudent(request,pk):

    user = User.objects.get(id=pk) 
    if user.is_coordinator:
        user.is_activated = False
        user.save()
        return redirect('AdminList')
    elif user.is_student:
        user.is_activated = False
        user.save()
        return redirect('AdminStudList')

def ManageStudentUpload(request):
   
    if request.user.is_coordinator:
       user_college = request.user.college
       IP = IntellectualProperty.objects.filter( is_pending = True , college=user_college)
    elif request.user.is_superuser:
       IP = IntellectualProperty.objects.filter(is_pending = True)
    
    
    
    context={'IP': IP }
    return render(request,'AdminCoor/manageStudUpload.html',context)


def viewIP(request):
    
    
    query = request.GET.get('q', '')  
    search_performed = False


  

    if query:
        
        filtered_IP = IntellectualProperty.objects.filter(
            Q(type__type__icontains=query), is_approved = True
          
          
        )

        filtered_IP_list = list(filtered_IP)

        seen_titles = set()
        unique_IPs = []
        for ip in filtered_IP_list:
            if ip.tittle not in seen_titles:
                unique_IPs.append(ip)
                seen_titles.add(ip.tittle)

        approvedIP = [ip for ip in unique_IPs if ip.is_approved]
        search_performed = True
    
   
    IP = IntellectualProperty.objects.all()
    ListofIP = [ L for L in IP if L.is_approved==True]


    displayIPlist=[]

    if search_performed:
       for ip in approvedIP:
           displayIPlist.append(ip)
    elif not search_performed:
        for ip in ListofIP:
           displayIPlist.append(ip)



 
    context = {
    'displayIPlist': displayIPlist, 
   

   
    }
    return render(request,'AdminCoor/viewIP.html',context)


def approveUpload(request,pk):
    
    IP = IntellectualProperty.objects.get(id=pk) 
    list_of_tokens = preprocess_doc_tokens(IP.file)
    IP.doc_text_tokens = json.dumps(list_of_tokens)
    IP.is_approved = True
    IP.is_pending = False
    IP.approvedBy = request.user
    IP.approvedDate = timezone.now()
    print(IP.approvedBy )
    IP.save()
    return redirect('AdminManageStudUpload')

def checkPlagiarism(request, pk):
    IP = IntellectualProperty.objects.get(id=pk)
    list_of_tokens = preprocess_doc_tokens(IP.file)
    IP.doc_text_tokens = json.dumps(list_of_tokens)
    IP.save()
    highest_score, highest_score_target = calc_doc_similarity(IP)
    IP.save()
    print(highest_score_target)
    source = ''
    if highest_score_target:
        source = IntellectualProperty.objects.get(tittle=highest_score_target)  
    else:
        source = None
    context = {'IP': IP,'highestscore' : highest_score * 100, 'source':source}
    return render(request,'AdminCoor/score.html',context)

    
def disapproveUpload(request,pk):

  
    IP = IntellectualProperty.objects.get(id=pk) 
    IP.is_approved = False
    IP.is_pending = False
    IP.disapprovedDate = timezone.now() 
    IP.save()

    frommail = settings.EMAIL_HOST_USER
    receiver = [IP.host.email]
    print(receiver)
    subject = "Disapproved"
    message = "WE regret to inform you that the abstract copy of work you uploaded was not approved by the coordinator for the reason that\
        it contain plagiarism rate of "
   
    send_mail(subject, message, frommail , receiver)    


    return redirect('AdminManageStudUpload')


def get_user_by_name(last_name, first_name):
    users = User.objects.filter(last_name__iexact=last_name, first_name__iexact=first_name)
    if users.exists():
        return users.first()
    return None
 

def AddIntellectualProperty(request, pk):
    
    if request.user.is_coordinator:
       form = IntellectualPropertyForm()
    elif request.user.is_superuser:
       form = AdminIntellectualPropertyForm()
       
    if request.method == 'POST':
        if request.user.is_coordinator:
           form = IntellectualPropertyForm(request.POST, request.FILES)
        elif request.user.is_superuser:
           form = AdminIntellectualPropertyForm(request.POST, request.FILES)
           
        if form.is_valid():
            IP = form.save(commit=False)
            if request.user.is_coordinator:
                user = User.objects.get(id=pk)
                IP.college=user.college
                IP.department=user.department
            IP.host = request.user
            IP.is_pending = True

            mainauthor_name = form.cleaned_data.get('mainauthor_username', '').strip()
            if mainauthor_name:
                try:
                    last_name, first_name = mainauthor_name.split(' ', 1)
                    mainauthor = get_user_by_name(last_name, first_name)
                    if mainauthor:
                        IP.mainauthor = mainauthor
                    else:
                        form.add_error('mainauthor_username', f'User with name "{mainauthor_name}" does not exist.')
                        return render(request, 'AdminCoor/AddIntellectualPropertyForm.html', {'form': form})
                except ValueError:
                    form.add_error('mainauthor_username', 'Please enter the name in "last_name first_name" format.')
                    return render(request, 'AdminCoor/AddIntellectualPropertyForm.html', {'form': form})
            else:
                IP.mainauthor = None

            IP.save()

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
                        form.add_error('author', f'User with name "{name}" does not exist.')
                        user_does_not_exist = True
                except ValueError:
                    form.add_error('author', f'Invalid name format "{name}". Use "last_name first_name".')
                    user_does_not_exist = True

            if user_does_not_exist:
                users = [request.user]

            IP.author.set(users)
            IP.save()

            if form.errors:
                return render(request, 'AdminCoor/AddIntellectualPropertyForm.html', {'form': form})

            return redirect('AdminIPList')
        else:
            messages.error(request, 'Failed to upload IP. Form returned None.')
    
    context = {'form': form}
    return render(request, 'AdminCoor/AddIntellectualPropertyForm.html', context)

def load_department(request):
    college_id = request.GET.get('college_id')
    departments = Department.objects.filter(college_id=college_id).all()

    type_id = request.GET.get('type_id')
    subtypes = SubType.objects.filter(type_id=type_id).all()

    context = {'departments': departments,
            'subtypes' : subtypes  }
    
    return render(request, 'AdminCoor/department_dropdown_list_options.html', context)



def intellectualProperty(request, pk):
   
   IP = IntellectualProperty.objects.get(id=pk)
   IP.ipviews += 1
   print(IP.ipviews)
 
   comments = IP.comment_set.all().order_by('created')
   

   time.sleep(3)
   IP.save()
 
   if request.method == 'POST':
       comments = Comment.objects.create(
           user = request.user,
           intellectualproperty=IP,
           content=request.POST.get('content')
           )
       return redirect('IntellectualProperty', pk=IP.id)
       

    
   context={
       'IP' : IP,
       'comments': comments,  
       
       
   }
   return render (request,'AdminCoor/IntellectualProperty.html',context)


