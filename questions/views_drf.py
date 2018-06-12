from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets

from questions.models import Question, Answer
from questions.serializers import QuestionSerializer, AnswerSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


def questions_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)


def question_detail(request, uid):
    try:
        question = Question.objects.get(pk=uid)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return JsonResponse(serializer.data)


def question_answers(request, uid):
    answers = Answer.objects.filter(question__id=uid).select_related('author', 'author__profile')\
        .order_by('-is_solution', 'created')
    if not answers:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AnswerSerializer(answers, many=True)
        return JsonResponse(serializer.data, safe=False)
