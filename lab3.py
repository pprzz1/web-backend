from flask import Blueprint, url_for, redirect, render_template, request, make_response

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('/lab3/lab3.html', name=name, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
        
    age = request.args.get('age')
    if user == '':
        errors['age'] = 'Заполните поле!'
        
    sex = request.args.get('sex')
    return render_template('/lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')

price = 0
@lab3.route('/lab3/pay')
def pay():
    global price
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('/lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    global price
    return render_template('/lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    text_align = request.args.get('text_align')

    if color or background_color or font_size or text_align:
        resp = make_response(render_template(
            'lab3/settings.html',
            color=color,
            background_color=background_color,
            font_size=font_size,
        ))
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp

    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')

    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        background_color=background_color,
        font_size=font_size,
    ))
    return resp

errors = {}
@lab3.route('/lab3/ticket')
def formTrain():
    ticketcost = 0
    fio = request.args.get('fio')
    place = request.args.get('place')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    start = request.args.get('start')
    end = request.args.get('end')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    argsNames = [fio, age, start, end, date]

    check = False

    if fio == '':
        errors['fio'] = 'Заполните поле!'
    else:
        errors['fio'] = ''

    if age == '':
        errors['age'] = 'Заполните поле!'
    elif  type(age) == str and (int(age) < 0 or int(age) > 120):
        errors['age'] = 'Возраст должен быть от 0 до 120 лет!'
    else:
        errors['age'] = ''

    if start == '':
        errors['start'] = 'Заполните поле!'
    else:
        errors['start'] = ''

    if end == '':
        errors['end'] = 'Заполните поле!'
    else:
        errors['end'] = ''

    if date == '':
        errors['date'] = 'Заполните поле!'
    else:
        errors['date'] = ''

    if all(argsNames) and (int(age) >= 0 and int(age) <= 120):
        check = True

    if check == True:
        if int(age) > 17:
            ticketcost += 1000
        else:
            ticketcost += 700

        if place == 'нижняя':
            ticketcost += 100
        elif place == 'нижняя боковая':
            ticketcost += 100
        
        if linen is not None:
            ticketcost += 75
        
        if luggage is not None:
            ticketcost += 250
        
        if insurance is not None:
            ticketcost += 150
        
    return render_template('lab3/ticket.html', fio=fio, place=place, linen=linen, luggage=luggage,
                        age=age, start=start, end=end, date=date, insurance=insurance, errors=errors,
                        argsNames=argsNames, check=check, ticketcost=ticketcost)