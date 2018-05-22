from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from questions.forms import SignUpForm


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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form,
                                                        'title': 'Sign Up',
                                                        })
