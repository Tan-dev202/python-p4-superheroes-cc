#!/usr/bin/env python3
from flask import Flask, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)


db.init_app(app)


@app.route('/')
def index():
    return '<h1>Superheroes GET/POST/PATCH API</h1>'


@app.route('/heroes')
def heroes():
    heroes = [hero.to_dict(only=('id', 'name', 'super_name'))
              for hero in Hero.query.all()]
    return make_response(heroes, 200)


@app.route('/heroes/<int:id>')
def heroes_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return make_response(json.dumps({'error': 'Hero not found'}), 404, {'Content-Type': 'application/json'})

    hero_details = hero.to_dict(only=('id', 'name', 'super_name'))
    hero_details['hero_powers'] = [
        {
            'hero_id': hero_power.hero_id,
            'id': hero_power.id,
            'power': hero_power.power.to_dict(only=('description', 'id', 'name')),
            'power_id': hero_power.power_id,
            'strength': hero_power.strength
        }
        for hero_power in hero.hero_powers
    ]
    return make_response(hero_details, 200)


@app.route('/powers')
def powers():
    powers = [power.to_dict(only=('description', 'id', 'name'))
              for power in Power.query.all()]
    return make_response(powers, 200)


@app.route('/powers/<int:id>')
def power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return make_response(json.dumps({'error': 'Power not found'}), 404, {'Content-Type': 'application/json'})
    
    else:
        power_details = power.to_dict(only=('description', 'id', 'name'))
        return make_response(power_details, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
