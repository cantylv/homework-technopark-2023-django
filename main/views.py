from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q  # для сложных условий в методе filter
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from gainSkills.settings import LOGIN_URL

# для блокировки кроссдоменных переходов
from urllib.parse import urlsplit

from .models import *

from .forms import *


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

    # Валидация GET-параметра page
    if page > p.num_pages:
        page = p.num_pages
    if page <= 0:
        page = 1
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


# обрабатывает POST-запросы на добавление ответа, а также GET-запрос на отображение вопроса и его ответов
def question(req, question_id):
    if req.method == 'POST':
        pass
    else:
        pass

    try:
        found_q = Question.questManager.get(id=question_id)
    except ObjectDoesNotExist:
        return redirect('home')

    ans = Answer.ansManager.getAnswersByQuestId(question_id)
    context = paginate(ans, req)  # вернется список ответов на какой-то странице

    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)
    return render(req, 'main/public/question.html', {
        'question': found_q,
        'context': context,
        'data_user': data_user
    })


@login_required(login_url=f'{LOGIN_URL}')
# обрабатывает POST-запросы на изменение учетных данных, а также GET-запросы на получение профиля пользователя
def profile(req, username):
    data_user = {
        'user': req.user,
        'profile': Profile.objects.get(user=req.user.id)
    }
    if req.method == "POST":
        form = ChangeProfile(data=req.POST, files=req.FILES)
        if form.is_valid():
            form.save(req.user.id)
            user = User.objects.get(id=req.user.id)
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
                print(next_url)
                return redirect(next_url)
            else:
                print("eblan")
    else:
        form = AddAuthorizationForm()
    return render(req, 'main/public/authorization.html', {
        "form": form
    })


# обрабатывает POST-запросы на регистрацию пользователя, а также GET-запросы на получение пустой формы
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
                return redirect(reverse('profile'))
            except User.DoesNotExist:
                form.add_error(None, "Unexpected error, please try to register once more!")
    else:
        form = AddRegistrationForm()
    return render(req, 'main/public/registration.html', {
        "form": form
    })


@login_required(login_url=f'{LOGIN_URL}')
# обрабатывает POST-запросы на добавление запроса, а также GET-запросы на страницы с формой ввода вопроса
def ask(req):
    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)
    return render(req, 'main/public/ask.html', {
        'data_user': data_user
    })


@require_GET
def about(req):
    data_user = {'user': req.user}
    if req.user.is_authenticated:
        data_user['profile'] = Profile.objects.get(user=req.user.id)
    return render(req, 'main/public/about.html', {
        'data_user': data_user
    })


# Функции служебные
def page_404(req, exc):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')


def is_safe_url(url, allowed_hosts):
    parts = urlsplit(url)
    return parts.netloc in allowed_hosts
