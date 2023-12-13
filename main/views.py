from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render
from .models import *
from faker import Faker


def fillUsers() -> None:
    fake = Faker('en_US')
    for i in range(10000):
        user = Users()
        user.img = 'users/fitness.img'
        user.login = fake.unique.user_name()
        user.email = fake.unique.free_email()
        user.password = fake.password(length=10)
        user.date_reg = fake.date()
        user.rating = fake.pyint()
        user.save()


user = Users.objects.get(id=1)
best_users = Users.objects.order_by('-rating')[:10]
popular_tags =['docker', 'golang', 'database', 'python', 'django']


def listing(req):
    quests = Questions.objects.all()
    search_text = req.GET.get('search', None)
    sorting = req.GET.get('sorted', None)

    if search_text is not None:
        # нужно искать в теле и заголовке вопроса совпадение
        quests = [q for q in quests if search_text in q['text'] or search_text in q['title']]

    if sorting is not None:
        if sorting == 'newest':
            quests = sorted(quests, key=lambda x: x['date_create'])
        elif sorting == 'high_score':
            quests = sorted(quests, key=lambda x: x['like'], reverse=True)

    return render(req, 'main/public/listing.html', {
        'user': user,
        'questions': quests,
        'best_users': best_users,
        'popular_tags': popular_tags,
        'search_text': search_text,
        'sorting': sorting
    })


def question(req, question_id):
    found_q = next(q for q in Questions.objects.all() if q['id'] == question_id)
    if found_q['id'] == -1:  # если такого вопроса нет, то прокидываем страницу 404
        raise Http404()
    ans = [answer for answer in Answers.objects.all if answer['question_id'] == question_id]
    sort = req.GET.get('sorted', None)
    if sort is not None:
        if sort == 'high_score':
            ans = sorted(ans, key=lambda x: x['like'], reverse=True)
        elif sort == 'newest':
            ans = sorted(ans, key=lambda x: x['date_create'])
    return render(req, 'main/public/question.html', {
        'user': user,
        'question': found_q,
        'answers': ans,
        'best_users': best_users,
        'popular_tags': popular_tags,
    })


def profile(req, login):
    selected_user = next(u for u in Users.objects.all() if u['login'] == login)
    return render(req, 'main/public/profile.html', {
        'user': selected_user
    })


def tag(req, tag_name):
    tag_questions = tag_name.split('@')
    quests = [q for q in Questions.objects.all() if any(t.lower() in map(str.lower, q['tags']) for t in tag_questions)]
    count_tags = len(tag_questions)
    if len(tag_questions) == 1:
        tag_questions = tag_questions[0]

    sorting = req.GET.get('sorted', None)
    if sorting is not None:
        if sorting == 'newest':
            quests = sorted(quests, key=lambda x: x['date_create'])
        elif sorting == 'high_score':
            quests = sorted(quests, key=lambda x: x['like'], reverse=True)

    return render(req, 'main/public/tag_question.html', {
        'user': user,
        'questions': quests,
        'best_users': best_users,
        'popular_tags': popular_tags,
        'tags': tag_questions,
        'count_tags': count_tags
    })


def authorization(req):
    return render(req, 'main/public/authorization.html')


def registration(req):
    return render(req, 'main/public/registration.html', {
        'best_users': best_users
    })


def ask(req):
    return render(req, 'main/public/ask.html', {
        'user': user,
        'best_users': best_users,
        'popular_tags': popular_tags
    })


def about(req):
    return render(req, 'main/public/about.html', {
        'user': user,
    })


def page_404(req, exc):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
