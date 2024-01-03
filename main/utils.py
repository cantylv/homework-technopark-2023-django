from collections import namedtuple
from django.db import connection


def get_questions():
    with connection.cursor() as cursor:
        # Выполнение основного запроса
        cursor.execute("""
            SELECT 
                q.id,
                q.title,
                q.text,
                u.login,
                u.img,
                q.date_create,
                q.like,
                q.dislike,
                q.comment
            FROM questions q
            JOIN users u ON q.user_id = u.id
        """)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Добавление тегов к каждому вопросу
        for question in result:
            cursor.execute("""
                SELECT t.name
                FROM tagquestions tq
                JOIN tag t ON tq.tag_id = t.id
                WHERE tq.question_id = %s
            """, [question['id']])
            tags = cursor.fetchall()
            question['tags'] = [tag[0] for tag in tags]
            question['img'] = '/uploads/' + question['img']

    return result


def get_question_by_id(q_id):
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

        if not result:
            return result
        # Поскольку мы тянем из бд чисто данные, то префикс не добавляется автоматически
        for question in result:
            cursor.execute("""
                       SELECT t.name
                       FROM tagquestions tq
                       JOIN tag t ON tq.tag_id = t.id
                       WHERE tq.question_id = %s
                   """, [question['id']])
            tags = cursor.fetchall()
            question['tags'] = [tag[0] for tag in tags]
            question['img'] = '/uploads/' + question['img']

    return result


def get_question_by_tags(tags):
    with connection.cursor() as cursor:
        # Формируем строку с тегами для каждого запроса
        tags_str = ', '.join([f"'{_}'" for _ in tags])

        cursor.execute(f"""
            SELECT DISTINCT
                questions.id,
                questions.title,
                questions.text,
                users.login,
                users.img,
                questions.date_create,
                questions.like,
                questions.dislike,
                questions.comment
            FROM
                Tagquestions
                JOIN questions ON Tagquestions.question_id = questions.id
                JOIN tag ON Tagquestions.tag_id = tag.id
                JOIN users ON questions.user_id = users.id
            WHERE
                tag.name IN ({tags_str})
        """)

        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Поскольку мы тянем из бд чисто данные, то префикс не добавляется автоматически
        for question in result:
            cursor.execute("""
                SELECT t.name
                FROM tagquestions tq
                JOIN tag t ON tq.tag_id = t.id
                WHERE tq.question_id = %s
            """, [question['id']])
            tags = cursor.fetchall()
            question['tags'] = [tag[0] for tag in tags]
            question['img'] = '/uploads/' + question['img']

    return result


def get_answers_by_id(q_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT answers.text, "
            "users.login, "
            "users.img, "
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
