from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    hero_powers = db.relationship(
        'HeroPower', back_populates='hero', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Hero {self.name} aka {self.super_name}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    hero_powers = db.relationship(
        'HeroPower', back_populates='power', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Power {self.name}: {self.description}>'

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError(
                "Description must be present and at least 20 characters long")
        return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    def __repr__(self):
        return f"<HeroPower Hero ID={self.hero_id}, Power ID={self.power_id}, Strength={self.strength}>"

    @validates('strength')
    def validate_strength(self, key, strength):
        values = ['Strong', 'Weak', 'Average']
        if strength not in values:
            raise ValueError(f"Strength must be one of: {', '.join(values)}")
        return strength
