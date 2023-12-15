from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render
from .models import *

popular_tags = ['docker', 'golang', 'database', 'python', 'django']


def paginate(object_list, req, per_page=10):
    search_text = req.GET.get('search', None)
    sorting = req.GET.get('sorted', None)
    page = req.GET.get('page', 1)

    if search_text is not None:
        # нужно искать в теле и заголовке вопроса совпадение
        object_list = [q for q in object_list if search_text in q['text'] or search_text in q['title']]

    if sorting is not None:
        if sorting == 'newest':
            object_list = sorted(object_list, key=lambda x: x['date_create'])
        elif sorting == 'high_score':
            object_list = sorted(object_list, key=lambda x: x['like'], reverse=True)

    p = Paginator(object_list, per_page, orphans=per_page * 0.3)
    context = {
        'object_list': p.get_page(page),
        'paginator_btns': p.get_elided_page_range(page, on_each_side=1, on_ends=1)
    }
    return context


def listing(req):
    context = paginate(Questions.objects.all(), req)
    print(context)
    return render(req, 'main/public/listing.html', {
        'context': context,
        'popular_tags': popular_tags,
        'req': req,
    })


def question(req, question_id):
    found_q = Questions.objects.get(id=question_id)
    if found_q['id'] == -1:  # если такого вопроса нет, то прокидываем страницу 404 (надо уточнить насчет проверки)
        raise Http404()
    ans = Answers.objects.filter(question_id=question_id)
    context = paginate(ans, req)  # вернется список ответов на какой-то странице
    return render(req, 'main/public/question.html', {
        'question': found_q,
        'context': context,
        'popular_tags': popular_tags,
    })


def profile(req, login):
    selected_user = Users.objects.get(login=login)
    return render(req, 'main/public/profile.html', {
        'user': selected_user
    })


def tag(req, tag_name):
    tag_questions = tag_name.split('@')
    quests = [q for q in Questions.objects.all() if any(t.lower() in map(str.lower, q['tags']) for t in tag_questions)]
    count_tags = len(tag_questions)
    if len(tag_questions) == 1:
        tag_questions = tag_questions[0]

    context = paginate(quests, req)

    return render(req, 'main/public/tag_question.html', {
        'popular_tags': popular_tags,
        'tags': tag_questions,
        'count_tags': count_tags,
        'context': context
    })


def authorization(req):
    return render(req, 'main/public/authorization.html')


def registration(req):
    return render(req, 'main/public/registration.html')


def ask(req):
    return render(req, 'main/public/ask.html', {
        'popular_tags': popular_tags
    })


def about(req):
    return render(req, 'main/public/about.html')


def page_404(req, exc):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
