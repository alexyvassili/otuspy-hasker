from rest_framework import serializers

from django.contrib.auth.models import User
from questions.models import Question, Answer, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tagword')


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Question
        fields = ('id', 'title', 'author', 'content', 'tags', 'rating', 'votes')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'author', 'content', 'is_solution', 'rating')
