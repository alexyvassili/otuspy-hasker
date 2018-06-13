from django.http import HttpResponse, JsonResponse
from django.contrib.postgres.search import SearchVector

from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from questions.models import Question, Answer
from questions.serializers import QuestionSerializer, AnswerSerializer
from questions.views import _get_trending


@api_view(['GET',])
def questions_list(request):
    """Paginated list of all questions"""
    if request.method == 'GET':
        paginator = PageNumberPagination()
        questions = Question.objects.all()
        result_page = paginator.paginate_queryset(questions, request)
        serializer = QuestionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET',])
def question_detail(request, uid):
    """Detail of one question by id"""
    try:
        question = Question.objects.get(pk=uid)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return JsonResponse(serializer.data) #, safe=False)


@api_view(['GET',])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def question_answers(request, uid):
    """Question answers by question id"""
    answers = Answer.objects.filter(question__id=uid).select_related('author', 'author__profile')\
        .order_by('-is_solution', 'created')
    if not answers:
        return HttpResponse(status=404)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(answers, request)
        serializer = AnswerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET',])
def trending(request):
    """Trending questions"""
    if request.method == 'GET':
        trending = _get_trending()
        serializer = QuestionSerializer(trending, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET',])
def search(request):
    """Search query. Use /api/search/?q=query"""
    # Question.objects.filter(content__search='Javascript')
    search_query = request.GET.get('q')
    if not search_query:
        return HttpResponse(status=404, content=b"Empty query string. Use /api/search/?q=query for search")
    if search_query.startswith('tag:'):
        # тег идет после tag: строго без пробела как в гуглопоиске
        tagword = search_query[4:]
        searchv = SearchVector('tags')
        searchv.default_alias = 'tag_search'
        found = Question.objects.filter(tags__tagword__iexact=tagword).order_by('-rating', '-created')
    else:
        searchv = SearchVector('title', 'content')
        searchv.default_alias = 'question_search'
        found = Question.objects.annotate(search=searchv).filter(search=search_query)\
            .order_by('-rating', '-created')
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(found, request)
    serializer = QuestionSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
