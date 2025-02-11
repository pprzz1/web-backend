from flask import Blueprint, render_template, abort, request, jsonify
from random import randint

import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def lab():
    return render_template('/lab7/lab7.html')


films = [
    {
        'title': 'The Last Frontier',
        'title_ru': 'Последняя граница',
        'year': 2018,
        'description': (
            'Действие фильма разворачивается в постапокалиптическом мире, где человечество '
            'пытается выжить в условиях разрушенной цивилизации. Главный герой, бывший солдат, '
            'отправляется в опасное путешествие через зараженные территории, чтобы найти '
            'последний оплот человечества. Его путь полон опасностей, встреч с выжившими и '
            'монстрами, которые населяют этот мир. Фильм заставляет задуматься о ценности жизни '
            'и силе человеческого духа.'
        ),
    },
    {
        'title': 'Code Breakers',
        'title_ru': 'Взломщики кодов',
        'year': 2015,
        'description': (
            '"Взломщики кодов" - это остросюжетный триллер, рассказывающий о группе '
            'гениальных хакеров, которые решают взломать систему глобального контроля и '
            'освободить мир от тирании. Их миссия становится еще более сложной, когда они '
            'обнаруживают, что за их действиями следит тайная организация, готовая на все, '
            'чтобы сохранить статус-кво. Фильм наполнен интригами, быстрыми перестрелками '
            'и интеллектуальными дуэлями.'
        ),
    },
    {
        'title': 'The Forgotten City',
        'title_ru': 'Забытый город',
        'year': 2021,
        'description': (
            '"Забытый город" - это приключенческий фильм, который рассказывает о группе '
            'археологов, которые отправляются на поиски легендарного города, упоминаемого '
            'только в древних рукописях. Их путешествие полно опасностей, тайн и древних '
            'загадок, которые они должны разгадать, чтобы найти город. Фильм наполнен '
            'эпическими сценами, захватывающими открытиями и неожиданными поворотами, '
            'которые заставят зрителей держаться за кровать.'
        ),
    }
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id >= len(films):
        return abort(404)
    else:
        return films[id]
    

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id >= len(films):
        return abort(404)
    else:
        del films[id]
        return '', 204
    

lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id >= len(films):
        return abort(404)
    else:
        film = request.get_json()
        if film['description'] == '':
            return {'description': 'Заполните описание'}, 400
        films[id] = film
        return films[id]
    
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json() 
    if not film or not all(k in film for k in ('title', 'title_ru', 'year', 'description')):
        return abort(400, "Invalid film data")  
    
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    if film['title_ru'] and not film['title']:
        film['title'] = film['title_ru']
    films.append(film) 
    return {'id': len(films) - 1}, 201 