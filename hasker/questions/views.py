from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from questions.forms import SignUpForm, UserUpdateForm, UserProfileForm, NewQuestionForm
from questions.models import Profile, Tag, AVATAR_DEFAULT


def index(request):
    title = 'Home'
    return render(request, 'questions/index.html', locals())


def new(request):
    title = 'New'
    return render(request, 'questions/new.html', locals())


def question(request):
    title = 'Question'
    return render(request, 'questions/q.html', locals())


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
        else:
            pass
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'questions/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': f'@{request.user.username} Profile',
    })


@login_required
@transaction.atomic
def ask(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.author = User.objects.get(username=request.user)
            pub.save()
            pub.tags.clear()

            tags = str(request.POST.get('tags'))
            tags = [tag.strip() for tag in tags.split(',')]
            for tag in tags:
                obj, create = Tag.objects.get_or_create(tagword=tag)
                pub.tags.add(obj)
            pub.save()
            return redirect('question')
        else:
            print(form.errors)
    else:
        form = NewQuestionForm(instance=request.user)
    return render(request, 'questions/ask.html', {
        'form': form,
        'title': 'Ask',
    })


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
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form,
                                                        'title': 'Sign Up',
                                                        })

@login_required
def set_default_avatar(request):
    user_profile = Profile.objects.get(user=request.user)
    user_profile.avatar = AVATAR_DEFAULT
    user_profile.save()
    return redirect('user_profile')
