from django.shortcuts import render
from django.http import HttpResponse

from os import listdir
from os.path import isdir

projlist = [dir for dir in listdir() if isdir(dir)]

def index(request):
	return render(request, 'projects/index.html', {'current_page': 'portfolio'})
