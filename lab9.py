from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')


# Страница 2: Ввод возраста
@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = int(request.form['age'])
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)


# Страница 3: Ввод пола
@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.taste_or_beauty', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)


# Страница 4: Выбор между "Что-то вкусное" и "Что-то красивое"
@lab9.route('/lab9/taste_or_beauty', methods=['GET', 'POST'])
def taste_or_beauty():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    if request.method == 'POST':
        if 'choice' not in request.form:
            return "Пожалуйста, выберите вариант", 400
        choice = request.form['choice']
        return redirect(url_for('lab9.detail_choice', name=name, age=age, gender=gender, choice=choice))
    return render_template('lab9/taste_or_beauty.html', name=name, age=age, gender=gender)


# Страница 5: Детали выбора
@lab9.route('/lab9/detail_choice', methods=['GET', 'POST'])
def detail_choice():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    choice = request.args.get('choice')
    if request.method == 'POST':
        if 'detail' not in request.form:
            return "Пожалуйста, выберите детали", 400
        detail = request.form['detail']
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, choice=choice, detail=detail))
    return render_template('lab9/detail_choice.html', name=name, age=age, gender=gender, choice=choice)


# Страница 6: Поздравление с подарком
@lab9.route('/lab9/congratulations', methods=['GET'])
def congratulations():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    choice = request.args.get('choice')
    detail = request.args.get('detail')
    # Логика выбора подарка
    if choice == 'вкусное':
        if detail == 'сладкое':
            gift = 'Мешочек конфет'
            image = 'candy.jpg'
        elif detail == 'сытное':
            gift = 'Пицца'
            image = 'pizza.jpg'
    elif choice == 'красивое':
        if detail == 'роскошное':
            gift = 'Браслет из золота' if gender == 'мужчина' else 'Золотое колье'
            image = 'gold_bracelet.jpg' if gender == 'мужчина' else 'gold_necklace.jpg'
        elif detail == 'стильное':
            gift = 'Сумка' if gender == 'женщина' else 'Куртка'
            image = 'bag.jpg' if gender == 'женщина' else 'jacket.jpg'
    # Поздравления для каждой категории
    if age <= 12:
        if gender == 'мужчина':
            message = f"Поздравляю тебя, {name}! Пусть твои мечты сбудутся, а впереди будет много побед, интересных приключений и новых достижений! Желаю, чтобы ты всегда был таким же веселым и активным! Вот тебе подарок — {gift}."
        else:
            message = f"Поздравляю тебя, {name}! Пусть в твоей жизни будет много радости, улыбок и волшебных моментов! Желаю расти умной, красивой и уверенной в себе девочкой! Вот тебе подарок — {gift}."
    else:
        if gender == 'мужчина':
            message = f"Поздравляю тебя, {name}! Пусть этот год принесет тебе много удачи и успешных начинаний! Желаю всегда быть сильным, уверенным и достигать больших целей! Твой подарок — {gift}!"
        else:
            message = f"Поздравляю тебя, {name}! Пусть твоя жизнь будет наполнена счастьем, гармонией и красивыми моментами. Желаю здоровья, любви и успехов во всем! Твой подарок — {gift}!"
    return render_template('lab9/congratulations.html', name=name, gift=gift, image=image, message=message)