from django.http import HttpResponse
from django.template import loader

def viewIPAsset(request):
  
  template = loader.get_template('viewIPAsset.html')
  return HttpResponse(template.render())