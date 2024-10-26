from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
      path = url_for("static", filename = "404.jpg")
      style = url_for("static", filename = "lab1.css")
      return '''
<!doctype html>
<html>
<head>
    <link rel = "stylesheet" href="''' + style +'''"
</head>
    <body>
        <img src="''' + path + '''" class="full-screen-image">
    </body>
</html>
''', 404

@app.route('/')
@app.route('/index')
def index():
    style = url_for("static", filename = "lab1.css")
    return '''<!doctype html>
        <html>
        <head>
            <link rel = "stylesheet" href="''' + style +'''"
            <meta charset="UTF-8">
            <title>Безделов Роман Артемович. Лабораторная работа 1</title>
        </head>
           <header>
                НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
           </header>
           <body>
                <a href='/lab1'>Первая лабораторная</a>
           </body>
           <footer>Безделов Роман Артемович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/lab1')
def lab1():
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
                <ul>
                    <li><a href="/">Главная страница</a></li>
                    <li><a href="/index">Главная страница (index)</a></li>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab1/web">Web</a></li>
                    <li><a href="/lab1/author">Автор</a></li>
                    <li><a href="/lab1/oak">Дуб</a></li>
                    <li><a href="/lab1/counter">Счетчик</a></li>
                    <li><a href="/lab1/reset_counter">Сброс счетчика</a></li>
                    <li><a href="/lab1/info">Информация</a></li>
                    <li><a href="/lab1/created">Создано успешно</a></li>
                    <li><a href="/error/400">Ошибка 400</a></li>
                    <li><a href="/error/401">Ошибка 401</a></li>
                    <li><a href="/error/402">Ошибка 402</a></li>
                    <li><a href="/error/403">Ошибка 403</a></li>
                    <li><a href="/error/405">Ошибка 405</a></li>
                    <li><a href="/error/418">Ошибка 418</a></li>
                    <li><a href="/trigger_error">Триггер ошибки</a></li>
                    <li><a href="/stone">Камень</a></li>
                </ul>
           </body>
           <footer>Безделов Роман Артемович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200

@app.route('/lab1/web')
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

@app.route('/lab1/author')
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
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    style = url_for("static", filename='lab1.css')
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

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    reset_link = url_for('reset_counter')   
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

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route('/lab1/info')
def info():
    return redirect('/lab1/author')

@app.route("/lab1/created")
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

@app.route('/error/400')
def error_400():
    return 'Bad Request', 400
@app.route('/error/401')
def error_401():
    return 'Unauthorized', 401
@app.route('/error/402')
def error_402():
    return 'Payment Required', 402
@app.route('/error/403')
def error_403():
    return 'Forbidden', 403
@app.route('/error/405')
def error_405():
    return 'Method Not Allowed', 405
@app.route('/error/418')
def error_418():
    return "I'm a teapot", 418

@app.route('/trigger_error')
def trigger_error():
    return 1 / 0
@app.errorhandler(500)
def internal_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
    </head>
    <body>
        <h1>Произошла ошибка на сервере</h1>
        <p>Пожалуйста, попробуйте позже.</p>
    </body>
</html>
''', 500

@app.route('/stone')
def heavy_metal():
    path = url_for("static", filename = "stone.jpg")
    style = url_for("static", filename = "lab1.css")
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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404 
    else:
        return 'цветок: ' + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<string:name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)} </p>
    <p>Полный список: {flower_list} </p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Рома Безделов'
    num_lab = 2
    group = 'ФБИ-22'
    num_course = 3
    return render_template('example.html', name=name, num_lab= num_lab, group=group, num_course=num_course)