from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    title = 'Home'
    return render(request, 'questions/index.html', locals())