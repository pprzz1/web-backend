from flask import Blueprint, render_template, request
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return  render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return  render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    operation = request.form.get('operation')
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if operation == 'sum':
        result = x1 + x2
    elif operation == 'mul':
        result = x1 * x2
    elif operation == 'sub':
        result = x1 - x2
    elif operation == 'pow':
        if x1 == 0 and x2 == 0:
            return render_template('lab4/div.html', error='Невозможно возвести 0 в степень 0!')
        result = x1 ** x2
    elif operation == 'div':
        if x2 == 0:
            return render_template('lab4/div.html', error='На ноль делить нельзя!')
        result = x1 / x2
    else:
        return render_template('lab4/div.html', error='Неизвестная операция!')
    return render_template('lab4/div.html', operation=operation, x1=x1, x2=x2, result=result)