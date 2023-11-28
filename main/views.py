from django.shortcuts import render
import random

questions = []
for i in range(0, 30):
    questions.append({
        'id': i,
        'title': 'title ' + str(i),
        'text': 'text ' + str(i),
        'user_ava': f'img/users/user{i % 10 + 1}_ava.jpg',
        'username': f'user_name{i}',
        'last_updated': random.randint(1, 59),
        'like': random.randint(0, 100),
        'dislike': random.randint(0, 100),
        'comment': random.randint(0, 1000),
        'question_tags': [random.choice(['django', 'python', 'go']), 'docker']
    })

answers = []
for i in range(0, 100):
    answers.append({
        'id': i,
        'question_id': random.randint(0, 30),
        'text': 'random text' + str(i),
        'user_ava': f'img/users/user{i % 10 + 1}_ava.jpg',
        'username': f'username{i}',
        'last_updated': random.randint(1, 59),
        'like': random.randint(0, 100),
        'dislike': random.randint(0, 100),
        'correct': bool(random.randint(0, 1))
    })

best_users = []
for i in range(1, 11):
    best_users.append({
        'username': f'user_name{i}',
        'user_ava': f'img/users/user{i}_ava.jpg'
    })

users = []
for i in range(1, 11):
    users.append({
        'id': i,
        'user_ava': f'img/users/user{i % 10 + 1}_ava.jpg',
        'username': f'username{i}',
        'login': f'login{i}',
        'email': f'user{i}@mail.ru',
        'user_token': 'XXX'
    })

popular_tags = ['Django', 'Python', 'Docker', 'C++', 'Centrifugo 3',
                'TP Web', 'Webpack', 'Jinja2', 'Golang', 'OS']

user = random.choice(users)  # наш пользователь в системе


def listing(req):
    quests = questions
    if req.GET.get('title') != 0:
        quests = [q for q in questions if req.GET.get('title') in q['title']]
    return render(req, 'main/public/listing.html', {
        'user': user,
        'questions': quests,
        'best_users': best_users,
        'popular_tags': popular_tags
    })


def question(req, question_id):
    print(question_id)
    found_q = next(q for q in questions if q['id'] == question_id)
    print(found_q)
    ans = [answer for answer in answers if answer['question_id'] == question_id]
    return render(req, 'main/public/question.html', {
        'user': user,
        'question': found_q,
        'answers': ans,
        'best_users': best_users,
        'popular_tags': popular_tags,
    })


def profile(req, login):
    selected_user = next(u for u in users if u['login'] == login)
    return render(req, 'main/public/profile.html', {
        'user': selected_user
    })


def tag(req, tag_name):
    tag_questions = [q for q in questions if tag_name in q['question_tags']]
    return render(req, 'main/public/tag_question.html', {
        'user': user,
        'questions': tag_questions,
        'best_users': best_users,
        'popular_tags': popular_tags,
        'selected_tag': tag_name
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
