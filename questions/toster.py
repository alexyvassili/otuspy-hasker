import json
import re
import requests
from bs4 import BeautifulSoup

HOST = 'toster.ru'
URL = f"https://{HOST}/tag/%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/questions"

session = requests.Session()

headers = {
        'Host': HOST,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }


def get_tags(obj):
    tags_container = obj.find_all("nav", attrs={"class": "question__tags"})[0]
    tags = tags_container.find_all("li", attrs={"class": "tags-list__item"})
    tags = [tag.text.strip() for tag in tags]
    return tags


def get_title(obj):
    title = obj.find_all("h1", attrs={"class": "question__title"})[0]
    return title.text.strip()


def get_content(obj):
    content = obj.find_all("div", attrs={"class": "question__text"})[0]
    return content.text.strip()


def get_answers(obj):
    solutions_container = obj.find_all("div", attrs={"class": "section_solutions"})[0]
    solutions = solutions_container.find_all("div", attrs={"class": "answer__text"})
    solutions = [solution.text.strip() for solution in solutions]

    answers_container = obj.find_all("div", attrs={"class": "section_answers"})[0]
    answers = answers_container.find_all("div", attrs={"class": "answer__text"})
    answers = [answer.text.strip() for answer in answers]
    return solutions, answers


def get_question(url):
    s = session.get(url, headers=headers)
    bsObj = BeautifulSoup(s.text, "html.parser")
    question = {'tags': get_tags(bsObj),
                'title': get_title(bsObj),
                'content': get_content(bsObj),
                }
    solutions, answers = get_answers(bsObj)
    return question, solutions, answers


def get_q_urls(questions_page_url):
    s = session.get(questions_page_url, headers=headers)
    bsObj = BeautifulSoup(s.text, "html.parser")
    questions = bsObj.find_all("a", attrs={"class": "question__title-link"})
    urls = []
    for question in questions:
        urls.append(question['href'])

    print(len(urls), 'questions')
    return urls


def get_hundred_questions():
    print('SCRAPING TOSTER!')
    urls = get_q_urls(URL)
    for i in range(2, 6):
        urls += get_q_urls(f'{URL}?page={i}')

    print('len urls', len(urls))
    questions = []
    for i, url in enumerate(urls):
        question, solutions, answers = get_question(url)
        print('question', i, 'answers', len(answers), 'solutions', len(solutions))
        questions.append((question, solutions, answers))
    return questions
