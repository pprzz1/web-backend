from flask import Blueprint, url_for, redirect, render_template

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404 
    else:
        return 'цветок: ' + flower_list[flower_id]

    
# Добавление нового цветка
@lab2.route('/lab2/add_flower/<string:name>')
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


@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400


@lab2.route('/lab2/all_flowers')
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


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list = []
    all_flowers_link = url_for('lab2.all_flowers')
    return f'''
<!doctype html>
<html>
<body>
    <h1>Список цветов очищен</h1>
    <a href="{all_flowers_link}">Посмотреть все цветы</a>
</body>
</html>
'''


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_single_number(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


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


@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)


objects = [
    {"name": "Toyota Camry", "description": "Седан среднего класса с высоким уровнем комфорта и надежности.", "image": "lab2/toyota-camry.jpg"},
    {"name": "Honda Civic", "description": "Компактный седан с экономичным двигателем и современным дизайном.", "image": "lab2/honda-civic.jpg"},
    {"name": "Ford Mustang", "description": "Классический американский спорткар с мощным двигателем и агрессивным внешним видом.", "image": "lab2/ford-mustang.jpg"},
    {"name": "Tesla Model S", "description": "Электромобиль премиум-класса с высокой автономностью и передовыми технологиями.", "image": "lab2/tesla-model-s.jpg"},
    {"name": "BMW X5", "description": "Полноразмерный кроссовер с роскошным интерьером и высокими динамическими характеристиками.", "image": "lab2/bmw-x5.jpg"}
]


@lab2.route('/lab2/objects')
def show_objects():
    return render_template('objects.html', objects=objects)