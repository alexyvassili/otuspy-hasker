from faker import Faker
import random


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hasker.secrets import TEST_USERS_PASS
from questions.toster import get_hundred_questions

fake = Faker()


def fill_users():
    for _ in range(100):
        user = User.objects.create_user(fake.user_name(), password=TEST_USERS_PASS)
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


def fill_with_texts():
    toster_questions = get_hundred_questions()
    for quest, solutions, answers in toster_questions:
        quest_user = get_user()
        question = add_question(quest, quest_user)
        for solution in solutions:
            add_answer(solution, question, get_user(no_user=quest_user), is_solution=True)
        for answer in answers:
            add_answer(answer, question, get_user(no_user=quest_user), is_solution=False)


def like(post):
    user = get_user()
    post.dislikes.remove(user)
    post.likes.add(user)


def dislike(post):
    user = get_user()
    post.likes.remove(user)
    post.dislikes.add(user)


def like_dislike(post, epsilon):
    for i in range(random.randint(1, epsilon)):
        like(post)
    for i in range(random.randint(1, epsilon // 2)):
        dislike(post)


def fill_with_likes(Post_model, max_rate):
    posts = Post_model.objects.all()
    for post in posts:
        like_dislike(post, random.randint(2, max_rate))
        post.rating = post.likes.count() - post.dislikes.count()
        post.save()


def fill_all():
    print('Creating users...')
    fill_users()
    print("Uploading Questions and answers...")
    fill_with_texts()
    print('Setting likes...')
    fill_with_likes(Question, 200)
    fill_with_likes(Answer, 100)
    print('Updating ratings...')
    posts = Question.objects.all()
    for post in posts:
        post.votes = post.likes.count() + post.dislikes.count()
        post.save()


class Command(BaseCommand):
    help = "create demodata in your db from toster.ru"

    def handle(self, **options):
        fill_all()
