from flask import Flask, url_for, redirect, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

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
                <br>
                <a href='/lab2'>Вторая лабораторная</a>
           </body>
           <footer>Безделов Роман Артемович, ФБИ-22, 3 курс, 2024</footer>
        </html>''', 200


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
    
# Добавление нового цветка
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

@app.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400

@app.route('/lab2/all_flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
<body>
    <h1>Все цветы</h1>
    <p>Всего цветов: {len(flower_list)}</p>
    <ul>
        {"".join([f"<li>{flower}</li>" for flower in flower_list])}
    </ul>
</body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    all_flowers_link = url_for('all_flowers')
    return f'''
<!doctype html>
<html>
<body>
    <h1>Список цветов очищен</h1>
    <a href="{all_flowers_link}">Посмотреть все цветы</a>
</body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Рома Безделов'
    num_lab = 2
    group = 'ФБИ-22'
    num_course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': '100'},
        {'name': 'груши', 'price': '120'},
        {'name': 'апедьсины', 'price': '90'},
        {'name': 'мандарины', 'price': '150'},
        {'name': 'манго', 'price': '70'}
    ]
    return render_template('example.html', name=name, num_lab= num_lab, group=group, num_course=num_course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

# Роут для математических операций с двумя числами
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    sum_result = a + b
    sub_result = a - b
    mul_result = a * b
    div_result = a / b if b != 0 else "Деление на ноль"
    pow_result = a ** b
    
    return f'''
<!doctype html>
<html>
<body>
    <h1>Результаты математических операций</h1>
    <p>Сумма: {a} + {b} = {sum_result}</p>
    <p>Разность: {a} - {b} = {sub_result}</p>
    <p>Произведение: {a} * {b} = {mul_result}</p>
    <p>Деление: {a} / {b} = {div_result}</p>
    <p>Возведение в степень: {a}<sup>{b}</sup> = {pow_result}</p>
</body>
</html>
'''

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_single_number(a):
    return redirect(url_for('calc', a=a, b=1))

books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Научная фантастика", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 158},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 448},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 448},
    {"author": "Антуан де Сент-Экзюпери", "title": "Маленький принц", "genre": "Философская сказка", "pages": 96},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Роман", "pages": 336}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

objects = [
    {"name": "Toyota Camry", "description": "Седан среднего класса с высоким уровнем комфорта и надежности.", "image": "toyota-camry.jpg"},
    {"name": "Honda Civic", "description": "Компактный седан с экономичным двигателем и современным дизайном.", "image": "honda-civic.jpg"},
    {"name": "Ford Mustang", "description": "Классический американский спорткар с мощным двигателем и агрессивным внешним видом.", "image": "ford-mustang.jpg"},
    {"name": "Tesla Model S", "description": "Электромобиль премиум-класса с высокой автономностью и передовыми технологиями.", "image": "tesla-model-s.jpg"},
    {"name": "BMW X5", "description": "Полноразмерный кроссовер с роскошным интерьером и высокими динамическими характеристиками.", "image": "bmw-x5.jpg"}
]

@app.route('/lab2/objects')
def show_objects():
    return render_template('objects.html', objects=objects)