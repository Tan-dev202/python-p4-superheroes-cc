#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return '<h1>Superheroes GET/POST/PATCH API</h1>'


@app.route('/heroes')
def heroes():
    heroes = [hero.to_dict(only=('id', 'name', 'super_name')) for hero in Hero.query.all()]
    return jsonify(heroes), 200


@app.route('/heroes/<int:id>')
def heroes_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

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
    return jsonify(hero_details), 200


@app.route('/powers')
def powers():
    powers = [power.to_dict(only=('description', 'id', 'name')) for power in Power.query.all()]
    return jsonify(powers), 200


@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    if request.method == 'GET':
        return jsonify(power.to_dict(only=('description', 'id', 'name'))), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict(only=('id', 'name', 'description'))), 200
        except ValueError as exc:
            db.session.rollback()
            return jsonify({'errors': str(exc)}), 400


@app.route('/hero_powers', methods=['POST'])
def add_hero_power():
    data = request.get_json()
    fields = ['strength', 'power_id', 'hero_id']
    for field in fields:
        if field not in data:
            return jsonify({'errors': [f'{field} is required']}), 400

    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    try:
        hero_power = HeroPower(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )
        db.session.add(hero_power)
        db.session.commit()

        hero_power_details = hero_power.to_dict(only=('id', 'hero_id', 'power_id', 'strength'))
        hero_power_details['hero'] = hero_power.hero.to_dict(only=('id', 'name', 'super_name'))
        hero_power_details['power'] = hero_power.power.to_dict(only=('id', 'name', 'description'))

        return jsonify(hero_power_details), 201

    except ValueError as exc:
        db.session.rollback()
        return jsonify({'errors': str(exc)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
