from rest_framework import serializers

from questions.models import Question, Answer, Tag


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'content', 'tags', 'rating', 'votes')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'author', 'content', 'is_solution', 'rating')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tagword')
