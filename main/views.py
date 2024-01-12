from django.core.exceptions import FieldError
from django.core.paginator import Paginator
from django.db.models import Q  # для сложных условий в методе filter
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from .models import *


# проверять валидность per_page и ограничить кол-во выводимых элементов <=100 не будем, так как это зашито в бэке
def paginate(object_list, req, per_page=20):
    search_text = req.GET.get('search', None)
    sorting = req.GET.get('sorted', None)
    try:
        page = int(req.GET.get('page', 1))
    except ValueError:
        page = 1

    if search_text is not None:
        search_text_lower = search_text.lower()
        try:
            # icontains - функция, позволяющая игнорировать регистр
            object_list = object_list.filter(
                Q(text__icontains=search_text_lower) | Q(title__icontains=search_text_lower)
            )
        except FieldError:  # FieldError будет у ответов, так как у них нет поля title
            object_list = object_list.filter(text__icontains=search_text_lower)

    if sorting is not None:
        if sorting == 'newest':
            object_list = object_list.order_by('-date_create')
        elif sorting == 'high_score':
            object_list = object_list.order_by('-rating')

    # orphans - кол-во элементов, которое будет переноситься с последней страницы на предыдущую, если на последней
    # окажется <= orphans элементов
    p = Paginator(object_list, per_page, orphans=per_page * 0.3, allow_empty_first_page=True)

    object_list = p.get_page(page)
    # Валидация GET-параметра page
    if page > p.num_pages:
        page = p.num_pages
    if page <= 0:
        page = 1

    # Будем передавать значения GET-параметров в шаблон, поскольку они будут пропадать, если их не передавать в формы
    get_params = {
        'search': search_text,
        'sorted': sorting,
        'page': page
    }

    # Фильтрация заглушек "..."
    paginator_btns = p.get_elided_page_range(page, on_each_side=1, on_ends=1)
    paginator_btns = [btn if isinstance(btn, int) else '...' for btn in paginator_btns]

    context = {
        'get_params': get_params,
        'object_list': object_list,
        'paginator': {
            'btns': paginator_btns,
            'size': len(paginator_btns)
        }
    }
    return context


@require_GET
def listing(req):
    quest = Question.questManager.all()
    context = paginate(quest, req)
    return render(req, 'main/public/listing.html', {
        'context': context
    })


@require_GET
def question(req, question_id):
    try:
        found_q = Question.questManager.get(id=question_id)
    except (IndexError, Question.DoesNotExist):
        return redirect('home')
    ans = Answer.ansManager.getAnswersByQuestId(question_id)
    context = paginate(ans, req)  # вернется список ответов на какой-то странице
    return render(req, 'main/public/question.html', {
        'question': found_q,
        'context': context,
    })


@require_GET
def profile(req, username):
    try:
        selected_user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Если пользователя с указанным логином не существует, выполняем редирект
        return redirect('home')
    return render(req, 'main/public/profile.html', {
        'user': selected_user
    })


@require_GET
def tag(req, tag_name):
    # проверка на пустоту массива необязательна, поскольку эта функция не вызовется, если не будут переданы теги
    quests, tags = Question.questManager.getQuestionsByTag(tag_name)
    context = paginate(quests, req)
    return render(req, 'main/public/tag_question.html', {
        'tags': tags,
        'context': context
    })


def authorization(req):
    return render(req, 'main/public/authorization.html')


def registration(req):
    return render(req, 'main/public/registration.html')


def ask(req):
    return render(req, 'main/public/ask.html')


@require_GET
def about(req):
    return render(req, 'main/public/about.html')


# Функции служебные
def page_404(req, exc):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')
