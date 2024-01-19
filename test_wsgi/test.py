def app(environ, start_response):
    """Simplest possible application object"""
    # переменная environ содержит переменные окружения, созданные WSGI протоколом или Application Server-ом
    # получим метод запроса
    method = environ.get('REQUEST_METHOD')

    if method == 'POST':
        data_length = int(environ.get('CONTENT_LENGTH', 0))
        data = environ['wsgi.input'].read(data_length).decode('utf-8')
        print('POST-параметры: ', data)
    else:
        get_params = environ.get('QUERY_STRING', '')
        print('GET-параметры: ', get_params)

    data = b'Technopark 2023-2024!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data))),
        ('Technopark', 'I like it')
    ]
    start_response(status, response_headers)
    return iter([data])


application = app
