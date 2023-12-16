from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import *
from .utils import *


def paginate(object_list, req, per_page=10):
    search_text = req.GET.get('search', None)
    sorting = req.GET.get('sorted', None)
    page = req.GET.get('page', 1)

    if search_text is not None:
        search_text_lower = search_text.lower()
        # нужно искать в теле и заголовке вопроса совпадение
        object_list = [q for q in object_list if
                       search_text_lower in q['text'].lower() or search_text_lower in q['title'].lower()]

    if sorting is not None:
        if sorting == 'newest':
            object_list = sorted(object_list, key=lambda x: x['date_create'])
        elif sorting == 'high_score':
            object_list = sorted(object_list, key=lambda x: x['like'], reverse=True)

    # orphans - кол-во элементов, которое будет переноситься с последней страницы на предыдущую, если на последней
    # окажется <= orphans элементов
    p = Paginator(object_list, per_page)

    # Фильтрация заглушек "..."
    paginator_btns = p.get_elided_page_range(page, on_each_side=1, on_ends=1)
    paginator_btns = [btn if isinstance(btn, int) else '...' for btn in paginator_btns]

    context = {
        'object_list': p.get_page(page),
        'paginator_btns': paginator_btns,
        'paginator_btns_size': len(paginator_btns)
    }
    return context


def listing(req):
    db = get_questions()  # уникальный запрос с JOIN on Users
    context = paginate(db, req)
    return render(req, 'main/public/listing.html', {
        'context': context,
        'req': req,
    })


def question(req, question_id):
    found_q = get_question_by_id(question_id)[0]
    # if found_q.id == -1: если такого вопроса нет, то прокидываем страницу 404 (надо уточнить насчет проверки)
    #     raise Http404()
    ans = get_answers_by_id(question_id)
    context = paginate(ans, req)  # вернется список ответов на какой-то странице
    return render(req, 'main/public/question.html', {
        'question': found_q,
        'context': context,
    })


def profile(req, login):
    selected_user = Users.objects.get(login=login)
    return render(req, 'main/public/profile.html', {
        'user': selected_user
    })


def tag(req, tag_name):
    tag_questions = tag_name.split('@')
    # нужно создать таблицу с тегами и таблицу для связи м-м с вопросами и тегами
    # нужно будет делать sql-запрос
    print(tag_questions)
    quests = get_question_by_tags(tag_questions)
    count_tags = len(tag_questions)
    if len(tag_questions) == 1:
        tag_questions = tag_questions[0]

    context = paginate(quests, req)

    return render(req, 'main/public/tag_question.html', {
        'tags': tag_questions,
        'count_tags': count_tags,
        'context': context
    })


def authorization(req):
    return render(req, 'main/public/authorization.html')


def registration(req):
    return render(req, 'main/public/registration.html')


def ask(req):
    return render(req, 'main/public/ask.html')


def about(req):
    return render(req, 'main/public/about.html')


def page_404(req, exc):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
