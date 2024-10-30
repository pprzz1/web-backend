from flask import Blueprint, url_for, redirect

lab1 = Blueprint('lab1', __name__)


@lab1.route('/lab1')
def lab():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <title>Лабораторная 1</title>
        </head>
           <body>
                <p>
                    Flask — фреймворк для создания веб-приложений на языке
                    программирования Python, использующий набор инструментов
                    Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                    называемых микрофреймворков — минималистичных каркасов
                    веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">Главная страница</a>
                <h2>Список роутов</h2>
                    <li><a href="/lab1/web">Web</a></li>
                    <li><a href="/lab1/author">Автор</a></li>
                    <li><a href="/lab1/oak">Дуб</a></li>
                    <li><a href="/lab1/counter">Счетчик</a></li>
                    <li><a href="/lab1/reset_counter">Сброс счетчика</a></li>
                    <li><a href="/lab1/info">Информация</a></li>
                    <li><a href="/lab1/created">Создано успешно</a></li>
                    <li><a href="/trigger_error">Триггер ошибки</a></li>
                    <li><a href="/lab1/stone">Камень</a></li>
                </ul>
           </body>
           <footer>Безделов Роман Артемович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200


@lab1.route('/lab1/web')
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-type': 'text/plain; charset=utf-8'
        }


@lab1.route('/lab1/author')
def author():
    name = "Безделов Рома Артемович"
    group = "ФБИ-22"
    faculty = "ФБ" 
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1">Главная страница</a>
            </body>
        </html>"""


@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    style = url_for("static", filename='lab1/lab1.css')
    return '''
        <!doctype html>
        <html>
        <head><link href="''' + style + '''" rel="stylesheet"></head>
            <body>
                <h1>Дуб</h1>
                <img src="''' + path + '''" class="oak-image">
            </body>
        </html>
        ''' 

count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    reset_link = url_for('lab1.reset_counter')   
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <br>
        <a href="''' + reset_link + '''">Очистить счётчик</a>
    </body>
</html>
    '''


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('lab1.counter'))


@lab1.route('/lab1/info')
def info():
    return redirect('/lab1/author')


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создан успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
    ''', 201


@lab1.route('/trigger_error')
def trigger_error():
    return 1 / 0


@lab1.route('/lab1/stone')
def stone():
    path = url_for("static", filename = "lab1/stone.jpg")
    style = url_for("static", filename = "lab1/lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel = "stylesheet" href="''' + style +'''"
        <meta charset="UTF-8">
        <title>Камень не дам</title>
    </head>
    <body>
        <h1>Плотину надо поднять.</h1>
        <p>
            Рычагом.
        </p>
        <p>
            Я его дам.
        </p>
        <p>
            Канал нужно завалить Камнем.
        </p>
        <p>
            Камень я не дам.
        </p>
        <img src="''' + path + '''" alt="Stone">
    </body>
</html>
''', 200, {
    'Content-Language': 'ru',
    'X-Custom-Header-1': 'Stone',
    'X-Custom-Header-2': 'Reptilia'
}