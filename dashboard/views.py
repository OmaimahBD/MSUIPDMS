from django.http import HttpResponse
from django.template import loader

def guest(request):
  
  template = loader.get_template('guestDashboard.html')
  return HttpResponse(template.render())