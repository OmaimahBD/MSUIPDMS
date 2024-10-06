from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render, redirect


from django.http import HttpResponse
from django.template import loader

def view(request):
  
  template = loader.get_template('viewPublishedResearch.html')
  return HttpResponse(template.render())

