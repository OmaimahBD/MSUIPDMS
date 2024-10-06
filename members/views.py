from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.contrib.auth.forms import UserCreationForm #login
from django.contrib.auth import authenticate, login    #login
from django.shortcuts import render, redirect          #login, register

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers, 
  }
  return HttpResponse(template.render(context, request))


def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')  
  context = {
    'mymember' : mymember ,
  }
  return HttpResponse(template.render(context,request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  mymembers = Member.objects.all().values()
  templatee = loader.get_template('template.html')
  context = {
    'fruits': ('banana','apple','orange','cherry', 'durian'),
    'mymembers': mymembers, 
  }
  return HttpResponse(templatee.render(context, request))


def _login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main') 
        else:
            error = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')


def _register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # go diregctly to the login page after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})