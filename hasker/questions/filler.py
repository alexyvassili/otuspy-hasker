import os
import django
from faker import Faker
import random

from questions.toster import get_hundred_questions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hasker.settings")
django.setup()
fake = Faker()

from django.contrib.auth.models import User


def fill_users():
    for _ in range(100):
        user = User.objects.create_user(fake.user_name(), password='qwe123')
        user.is_superuser=False
        user.is_staff=False
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.email = fake.email()
        user.profile.about = fake.sentence()
        user.save()


def get_user(no_user=None):
    users = User.objects.all()
    user = random.choice(users)
    if not user.is_staff and user != no_user:
        return user
    else:
        return get_user()

from questions.models import Question, Tag, Answer


def add_question(quest, user):
    question = Question.objects.create(author=user,
                                       title=quest['title'],
                                       content=quest['content'], )
    question.save()
    tags = quest['tags']
    for tag in tags:
        obj, create = Tag.objects.get_or_create(tagword=tag)
        question.tags.add(obj)
    question.save()
    return question

def add_answer(answer_text, question, user, is_solution):
    answer = Answer.objects.create(author=user,
                                   question=question,
                                   content=answer_text,
                                   is_solution=is_solution,)
    answer.save()


toster_questions = get_hundred_questions()
for quest, solutions, answers in toster_questions:
    quest_user = get_user()
    question = add_question(quest, quest_user)
    for solution in solutions:
        add_answer(solution, question, get_user(no_user=quest_user), is_solution=True)
    for answer in answers:
        add_answer(answer, question, get_user(no_user=quest_user), is_solution=False)


