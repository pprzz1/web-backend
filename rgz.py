from flask import Blueprint, render_template, request, redirect, session, current_app, url_for, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

cinema = Blueprint('cinema', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='cinema_db',
            user='roma_rgz',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "cinema.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def is_admin():
    return session.get('is_admin', False)

@cinema.route('/cinema/')
def index():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM sessions;")
    sessions = cur.fetchall()
    db_close(conn, cur)
    return render_template('cinema/index.html', sessions=sessions)

@cinema.route('/cinema/session/<int:session_id>', methods=['GET'])
def session_detail(session_id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM sessions WHERE id=%s;", (session_id,))
    session_data = cur.fetchone()

    if not session_data:
        db_close(conn, cur)
        return "Сеанс не найден", 404

    cur.execute("SELECT seat_number, user_id FROM bookings WHERE session_id=%s;", (session_id,))
    bookings = cur.fetchall()
    db_close(conn, cur)

    return render_template('cinema/session.html', session=session_data, bookings=bookings)

@cinema.route('/cinema/seats/<int:session_id>', methods=['GET'])
def get_seats(session_id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT seat_number, user_id FROM bookings WHERE session_id = %s", (session_id,))
    seats = [{"seat_number": row[0], "user_id": row[1]} for row in cur.fetchall()]
    
    return jsonify(seats)

@cinema.route('/book_seat/<int:session_id>', methods=['POST'])
def book_seat(session_id):
    conn = db_connect()
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "error": "Вы не авторизованы!"}), 403

    seat_number = request.form.get('seat_number')
    if not seat_number:
        return jsonify({"success": False, "error": "Некорректный номер места!"}), 400

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings WHERE user_id = %s AND session_id = %s", (user_id, session_id))
    if cur.fetchone()[0] >= 5:
        return jsonify({"success": False, "error": "Вы уже забронировали 5 мест!"}), 400

    cur.execute("SELECT COUNT(*) FROM bookings WHERE seat_number = %s AND session_id = %s", (seat_number, session_id))
    if cur.fetchone()[0] > 0:
        return jsonify({"success": False, "error": "Это место уже занято!"}), 400

    cur.execute("INSERT INTO bookings (user_id, session_id, seat_number) VALUES (%s, %s, %s)", (user_id, session_id, seat_number))
    conn.commit()

    return jsonify({"success": True})  # Отправляем успешный ответ


@cinema.route('/cinema/cancel/<int:booking_id>/<int:session_id>', methods=['POST'])
def cancel_booking(booking_id, session_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('cinema.login'))
    
    conn, cur = db_connect()
    cur.execute("SELECT user_id FROM bookings WHERE seat_number=%s AND session_id=%s;", (booking_id, session_id))
    booking = cur.fetchone()

    if not booking:
        db_close(conn, cur)
        return "Ошибка: Бронирование не найдено."

    if not session.get('is_admin') and booking["user_id"] != user_id:
        db_close(conn, cur)
        return "Ошибка: Вы не можете отменить это бронирование."

    cur.execute("DELETE FROM bookings WHERE seat_number=%s AND session_id=%s;", (booking_id, session_id))
    db_close(conn, cur)
    return redirect(url_for('cinema.session_detail', session_id=session_id))

@cinema.route('/cinema/logout')
def logout():
    session.pop('user_id', None)
    session.pop('login', None)
    session.pop('is_admin', None)
    return redirect(url_for('cinema.login'))

@cinema.route('/cinema/admin', methods=['GET'])
def admin_panel():
    if not is_admin():
        return redirect(url_for('cinema.login'))

    conn, cur = db_connect()
    cur.execute("SELECT * FROM sessions;")
    sessions = cur.fetchall()
    db_close(conn, cur)

    return render_template('cinema/admin.html', sessions=sessions)


@cinema.route('/cinema/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('cinema/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('cinema/login.html', error='Заполните все поля!')

    conn, cur = db_connect()
    cur.execute("SELECT id, login, password, is_admin FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if user is None or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('cinema/login.html', error='Логин и/или пароль неверны')

    session['user_id'] = user['id']
    session['login'] = user['login']
    session['is_admin'] = user['is_admin']
    db_close(conn, cur)

    return redirect(url_for('cinema.index'))


@cinema.route('/cinema/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('cinema/register.html')

    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')

    if not (name and login and password):
        return render_template('cinema/register.html', error='Заполните все поля!')

    conn, cur = db_connect()
    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('cinema/register.html', error="Такой пользователь уже существует!")

    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (name, login, password, is_admin) VALUES (%s, %s, %s, FALSE);", (name, login, password_hash))
    
    db_close(conn, cur)
    return redirect(url_for('cinema.login'))



