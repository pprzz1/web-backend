from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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
                <img src="''' + path + '''">
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
