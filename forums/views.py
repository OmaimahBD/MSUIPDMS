from django.http import HttpResponse
from django.template import loader

def forums(request):
  
  template = loader.get_template('forums.html')
  return HttpResponse(template.render())