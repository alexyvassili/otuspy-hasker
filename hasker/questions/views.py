from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    title = 'Home'
    return render(request, 'questions/index.html', locals())


def new(request):
    title = 'New'
    return render(request, 'questions/new.html', locals())


def question(request):
    title = 'Question'
    return render(request, 'questions/q.html', locals())


def ask(request):
    title = 'Ask'
    return render(request, 'questions/ask.html', locals())


def profile(request):
    title = 'User Profile'
    return render(request, 'questions/profile.html', locals())


def search(request):
    title = 'Search'
    return render(request, 'questions/search.html', locals())
