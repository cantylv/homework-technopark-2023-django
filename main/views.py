from gainSkills.settings import *
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q  # для сложных условий в методе filter
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from gainSkills.settings import LOGIN_URL

import django.contrib.postgres.search

from .forms import *

# для генерации JWT
import jwt
import time

import requests
import json


def get_centrifugo_data(user_id):
    user_id = 0 if user_id is None else user_id
    token = jwt.encode({"sub": str(user_id), "exp": int(time.time()) + 100 * 60}, TOKEN_HMAC_SECRET_KEY,
                       algorithm="HS256")
    return {
        "user_token": token,
        "ws_url": CENTRIFUGO_WS_URL,
    }


def ws_add_answer(answer, question_id):
    data = json.dumps({
        "channel": f"{question_id}",
        "data": {
            "answer": {
                "id": f"{answer.id}",
                "text": f"{answer.text}",
                "date_create": f"{answer.date_create}",
                "correct": f"{answer.correct}",
                "like": f"{answer.like}",
                "dislike": f"{answer.dislike}",
                "username": f"{answer.user.username}",
                "user_id": f"{answer.user.id}",
                "avatar": f"{answer.user.profile.avatar.url}"
            }
        }

    })
    headers = {'X-API-Key': f'{API_KEY}', 'Content-type': 'application/json'}
    requests.post(f"{CENTRIFUGO_WS_URL_PUBLISH_DATA}", data=data, headers=headers)


# проверять валидность per_page и ограничить кол-во выводимых элементов <=100 не будем, так как это зашито в бэке
def paginate(object_list, req, ans_id=None, per_page=10):
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

    # Валидация GET-параметра page
    if page > p.num_pages:
        page = p.num_pages
    if page <= 0:
        page = 1

    # находим страницу, на которую был добавлен ответ
    if ans_id is not None:
        try:
            ans = Answer.objects.get(id=ans_id)
            for i in p.page_range:
                if ans in p.page(i).object_list:
                    page = i
                    break
        except Answer.DoesNotExist:
            pass

    try:
        object_list = p.page(page)
    except EmptyPage:
        object_list = []

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
    # почему-то профиль отцепился от пользователя, поэтому сделаем запрос
    # проверять не будем, так как в момент регистрации было создание профиля для каждого пользователя
    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)
    return render(req, 'main/public/listing.html', {
        'context': context,
        'data_user': data_user
    })


@csrf_protect
def question(req, question_id):
    if req.method == 'POST':
        form = AddAnswerForm(req.POST)
        if form.is_valid():
            if req.user.is_authenticated:
                ans = form.save(question_id=question_id, user=req.user)
                # после добавления ответа нужно пересчитать рейтинг вопроса
                ans.question.comment += 1
                ans.question.countRating()
                ans.question.save()
                # обращаемся к Centrifugo
                ws_add_answer(ans, question_id)
                # Добавим данные в сессию
                req.session['ans_id'] = ans.id
                return redirect(reverse('question', kwargs={'question_id': question_id}))
            else:
                form.add_error(None, "You need to authorize!")
    else:
        form = AddAnswerForm()

    try:
        found_q = Question.questManager.get(id=question_id)
    except ObjectDoesNotExist:
        return redirect('home')

    ans = Answer.ansManager.getAnswersByQuestId(question_id).order_by('-correct')

    # Проверим, есть ли данные в сессии
    ans_id = req.session.pop('ans_id', None)

    if ans_id:
        context = paginate(ans, req, ans_id)
    else:
        context = paginate(ans, req)  # вернется список ответов на какой-то странице

    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)

    # придется тут сформировать context, потому что перед return его необходимо изменить при условии

    html_context = {
        'question': found_q,
        'context': context,
        'data_user': data_user,
        'form': form,
        'centrifugo': get_centrifugo_data(req.user.id)
    }

    if ans_id:
        html_context['ans_id'] = ans_id

    return render(req, 'main/public/question.html', html_context)


@login_required(login_url=f'{LOGIN_URL}')
@csrf_protect
# обрабатывает POST-запросы на изменение учетных данных, а также GET-запросы на получение профиля пользователя
def profile(req, username):
    data_user = {
        'user': req.user,
        'profile': Profile.objects.get(user=req.user.id)
    }
    if req.method == "POST":
        form = ChangeProfile(data=req.POST, files=req.FILES)
        if form.is_valid():
            user = form.save(req.user.id)
            update_session_auth_hash(req, user)
            return redirect(reverse('profile', kwargs={'username': req.user.username}))
        print(form.is_valid())
    else:
        form = ChangeProfile(initial={'username': req.user.username, 'email': req.user.email})
    return render(req, 'main/public/profile.html', {
        'data_user': data_user,
        'form': form
    })


@require_GET
def tag(req, tag_name):
    # проверка на пустоту массива необязательна, поскольку эта функция не вызовется, если не будут переданы теги
    quests, tags = Question.questManager.getQuestionsByTag(tag_name)
    context = paginate(quests, req)
    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)
    return render(req, 'main/public/tag_question.html', {
        'tags': tags,
        'context': context,
        'data_user': data_user
    })


# обрабатывает POST-запросы на аутентификацию пользователя, а также GET-запросы на получение пустой формы
@csrf_protect
def authorization(req):
    if req.user.is_authenticated:
        return redirect(reverse('home'))
    if req.method == "POST":
        form = AddAuthorizationForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                next_url = req.POST.get('next', '/')
                return redirect(next_url)
            else:
                print("eblan")
    else:
        form = AddAuthorizationForm()
    return render(req, 'main/public/authorization.html', {
        "form": form
    })


# обрабатывает POST-запросы на регистрацию пользователя, а также GET-запросы на получение пустой формы
@csrf_protect
def registration(req):
    if req.user.is_authenticated:
        return redirect(reverse('home'))
    if req.method == 'POST':
        form = AddRegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            try:
                username = form.cleaned_data['username']
                user = User.objects.get(username=username)
                login(req, user)
                return redirect(reverse('home'))
            except User.DoesNotExist:
                form.add_error(None, "Unexpected error, please try to register once more!")
    else:
        form = AddRegistrationForm()
    return render(req, 'main/public/registration.html', {
        "form": form
    })


@login_required(login_url=f'{LOGIN_URL}')
@csrf_protect
# обрабатывает POST-запросы на добавление запроса, а также GET-запросы на страницы с формой ввода вопроса
def ask(req):
    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)

    if req.method == 'POST':
        form = AddQuestionForm(req.POST)
        if form.is_valid():
            q = form.save(req.user)
            return redirect(reverse("question", kwargs={"question_id": q.id}))
    else:
        form = AddQuestionForm()
    return render(req, 'main/public/ask.html', {
        'data_user': data_user,
        'form': form
    })


@require_GET
def about(req):
    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)
    return render(req, 'main/public/about.html', {
        'data_user': data_user
    })


# выход еще не работает
@login_required(login_url=f'{LOGIN_URL}')
@csrf_protect
def user_logout(req):
    logout(req)
    return redirect(reverse('home'))


# для AJAX запросов
@login_required(login_url=f'{LOGIN_URL}')
@csrf_protect
def changeReaction(req):
    user = req.user
    body = req.body.decode('utf-8')  # Декодирование байтов в строку
    body_decoded = json.loads(body)  # Парсинг JSON

    object_id = body_decoded.get('object_id')
    operationType = body_decoded.get('operation')
    objectType = body_decoded.get('objectType')

    if objectType == 'Q':
        try:
            q = Question.objects.get(id=object_id)
        except Question.DoesNotExist:
            return JsonResponse({
                "status": 502,
                "needAddReaction": False,
                "message": "Object question does not exits"
            })

        if operationType == "L":
            queryset = LikeQuestion.objects.filter(user=user, question=q)
        else:
            queryset = DislikeQuestion.objects.filter(user=user, question=q)

        reaction_exist = queryset.exists()

        if reaction_exist:
            queryset.delete()
            if operationType == "L":
                q.like -= 1
            else:
                q.dislike -= 1
            needAddReaction = False
        else:
            if operationType == "L":
                LikeQuestion.objects.create(user=user, question=q)
                q.like += 1
            else:
                DislikeQuestion.objects.create(user=user, question=q)
                q.dislike += 1
            needAddReaction = True
        q.countRating()
        q.save()
    else:
        try:
            a = Answer.objects.get(id=object_id)
        except Answer.DoesNotExist:
            return JsonResponse({
                "status": 502,
                "needAddReaction": False,
                "message": "Object answer does not exist"
            })
        if operationType == "L":
            queryset = LikeAnswer.objects.filter(user=user, answer=a)
        else:
            queryset = DislikeAnswer.objects.filter(user=user, answer=a)

        reaction_exist = queryset.exists()
        if reaction_exist:
            queryset.delete()
            if operationType == "L":
                a.like -= 1
            else:
                a.dislike -= 1
            needAddReaction = False
        else:
            if operationType == "L":
                LikeAnswer.objects.create(user=user, answer=a)
                a.like += 1
            else:
                DislikeAnswer.objects.create(user=user, answer=a)
                a.dislike += 1
            needAddReaction = True
        a.countRating()
        a.save()
    return JsonResponse({
        "status": 200,
        "needAddReaction": needAddReaction,
        "message": "Operation has finished successful!"
    })


# для AJAX запросов
@login_required(login_url=f'{LOGIN_URL}')
@csrf_protect
def rightAnswer(req):
    body = req.body.decode('utf-8')  # Декодирование байтов в строку
    body_decoded = json.loads(body)  # Парсинг JSON
    answer_id = body_decoded['object_id']
    try:
        ans = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        return JsonResponse({
            "status": 502,
            "message": "Object answer does not exist!"
        })
    isChecked = ans.correct
    # меняем на противоположное значение
    ans.correct = False if isChecked else True
    ans.save()
    return JsonResponse({
        "status": 200,
        "isRightAnswer": ans.correct,
        "message": "Operation has finished successful!"
    })


# Функции служебные
def page_404(req, exc):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')
