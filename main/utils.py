from collections import namedtuple
from django.db import connection


def get_questions():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT questions.id, "
            "questions.title, "
            "questions.text, "
            "users.login as login, "
            "users.img as img, "
            "questions.date_create, "
            "questions.like,"
            "questions.dislike,"
            "questions.comment "
            "FROM questions JOIN users ON questions.user_id = users.id"
        )
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Поскольку мы тянем из бд чисто данные, то префикс не добавляется автоматически
        for question in result:
            question['img'] = '/uploads/' + question['img']
    return result


def get_question(q_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT questions.id, "
            "questions.title, "
            "questions.text, "
            "users.login as login, "
            "users.img as img, "
            "questions.date_create, "
            "questions.like,"
            "questions.dislike,"
            "questions.comment "
            "FROM questions JOIN users ON questions.user_id = users.id "
            f"WHERE questions.id = {q_id}"
        )
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Поскольку мы тянем из бд чисто данные, то префикс не добавляется автоматически
        for question in result:
            question['img'] = '/uploads/' + question['img']
    return result


def get_answers(q_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT answers.text, "
            "users.login as login, "
            "users.img as img, "
            "answers.date_create, "
            "answers.like,"
            "answers.dislike,"
            "answers.correct "
            "FROM answers JOIN users ON answers.user_id = users.id "
            f"WHERE answers.question_id = {q_id}"
        )
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Поскольку мы тянем из бд чисто данные, то префикс не добавляется автоматически
        for question in result:
            question['img'] = '/uploads/' + question['img']
    return result
