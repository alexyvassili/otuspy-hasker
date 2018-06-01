import json
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.contrib.postgres.search import SearchVector
from questions.forms import SignUpForm, UserUpdateForm, UserProfileForm, NewQuestionForm, NewAnswerForm
from questions.models import Profile, Tag, Question, Answer, AVATAR_DEFAULT


def index(request):
    questions = Question.objects.all().prefetch_related('tags').order_by('-votes')
    paginator = Paginator(questions, 20)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/index.html', {'questions': questions,
                                                    'title': 'Home',
                                                    'trending': _get_trending(),})


def new(request):
    questions = Question.objects.all().prefetch_related('tags').order_by('-created')
    paginator = Paginator(questions, 20)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/new.html', {'questions': questions,
                                                    'title': 'New Questions',
                                                    'trending': _get_trending(),})


def search(request):
    # Question.objects.filter(content__search='Javascript')
    search_query = request.GET.get('q')
    searchv = SearchVector('title', 'content')
    searchv.default_alias = 'question_search'
    found = Question.objects.annotate(search=searchv).filter(search=search_query).order_by('-rating')
    # search = Question.objects.all().prefetch_related('tags').order_by('-created')
    paginator = Paginator(found, 20)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/search.html', {'questions': questions,
                                                     'title': f'Search: "{search_query}"',
                                                     'search_query': search_query,
                                                     'count': paginator.count,
                                                     'trending': _get_trending(), })


def tag_search(request, tagword):
    searchv = SearchVector('tags')
    searchv.default_alias = 'tag_search'
    # found = Question.objects.annotate(search=searchv).filter(search=tagword).order_by('-rating')
    found = Question.objects.filter(tags__tagword__iexact=tagword).order_by('-created')
    paginator = Paginator(found, 20)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/tag.html', {'questions': questions,
                                                  'title': f'Tag: #{tagword}',
                                                  'tagword': tagword,
                                                  'count': paginator.count,
                                                  'trending': _get_trending(), })


@transaction.atomic
def question(request, uid):
    if request.method == 'POST':
        form = NewAnswerForm(request.POST)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.author = User.objects.get(username=request.user)
            pub.question = Question.objects.get(pk=uid)
            pub.save()
            return redirect('question', uid)
    else:
        question = get_object_or_404(Question, pk=uid)
        title = question.title
        is_owner = question.author.id == request.user.id
        # '-rating' change to 'created'
        answers = Answer.objects.filter(question__id=uid).order_by('-is_solution', 'created')
        form = NewAnswerForm()
        return render(request, 'questions/q.html', {'title': title,
                                                    'question': question,
                                                    'answers': answers,
                                                    'is_owner': is_owner,
                                                    'form': form,
                                                    'trending': _get_trending(),})


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
        'trending': _get_trending(),
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
            print(pub.id)
            return redirect('question', pub.id)
        else:
            print(form.errors)
    else:
        form = NewQuestionForm(instance=request.user)
    return render(request, 'questions/ask.html', {
        'form': form,
        'title': 'Ask',
        'trending': _get_trending(),
    })


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
                                                        'trending': _get_trending(),
                                                        })

@login_required
def set_default_avatar(request):
    user_profile = Profile.objects.get(user=request.user)
    user_profile.avatar = AVATAR_DEFAULT
    user_profile.save()
    return redirect('user_profile')


@login_required
def like_question(request, uid):
    user = request.user
    post = Question.objects.get(id=uid)
    post.dislikes.remove(user)
    post.likes.add(user)
    post.rating = post.likes.count() - post.dislikes.count()
    post.votes = post.likes.count() + post.dislikes.count()
    post.save()
    return HttpResponse(str(post.rating))


@login_required
def dislike_question(request, uid):
    user = request.user
    post = Question.objects.get(id=uid)
    post.likes.remove(user)
    post.dislikes.add(user)
    post.rating = post.likes.count() - post.dislikes.count()
    post.votes = post.likes.count() + post.dislikes.count()
    post.save()
    return HttpResponse(str(post.rating))


@login_required
def like_answer(request, ans_uid):
    user = request.user
    post = Answer.objects.get(id=ans_uid)
    post.dislikes.remove(user)
    post.likes.add(user)
    post.rating = post.likes.count() - post.dislikes.count()
    post.save()
    return HttpResponse(str(post.rating))


@login_required
def dislike_answer(request, ans_uid):
    user = request.user
    post = Answer.objects.get(id=ans_uid)
    post.likes.remove(user)
    post.dislikes.add(user)
    post.rating = post.likes.count() - post.dislikes.count()
    post.save()
    return HttpResponse(str(post.rating))


def send_all_tags(request):
    tags = Tag.objects.all()
    data = [tag.tagword for tag in tags]
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def _get_trending():
    """Чтобы трендинг не дублировал hot questions, он отражает вопросы с наибольшим числом
    голосов за последний месяц. И в том и в другом случае учитывается количество голоса, а не рейтинг
    Для еще большего различия в hot questions можно было бы добавлять не по голосам, а по рейтингу.
    """
    last_month = datetime.today() - timedelta(days=30)
    trending = Question.objects.filter(created__gte=last_month).order_by('-votes')[:15]
    return trending


@login_required
def set_answer_as_solution(request, ans_uid):
    user = request.user
    post = Answer.objects.get(id=ans_uid)
    if post.is_solution:
        return HttpResponse(f"Ne balyisya knopkoj, mudilo!")
    if post.question.author.id == user.id:
        post.is_solution = True
        post.save()
        return HttpResponse(f"OK. Set answer id {ans_uid} as solution")
    else:
        return HttpResponse(f"Error. You are not author of this question! Where are you find this button?")
