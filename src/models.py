# Converting model from tweet db to a lego parts db

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class PartType(db.Model):
    __tablename__ = 'part_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    parts = db.relationship('Part', backref='part_type', cascade='all,delete')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class Color(db.Model):
    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    hex_value = db.Column(db.String(7), unique=True, nullable=False)
    
    def __init__(self, name, hex_value):
        self.name = name
        self.hex_value = hex_value

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'hex_value': self.hex_value,
        }

class SizeCategory(db.Model):
    __tablename__ = 'size_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class Part(db.Model):
    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lego_item_number = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    part_type_id = db.Column(db.Integer, db.ForeignKey('part_types.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    size_category_id = db.Column(db.Integer, db.ForeignKey('size_categories.id'), nullable=False)

    def __init__(self, lego_item_number, name, description, part_type_id, color_id, size_category_id):
        self.lego_item_number = lego_item_number
        self.name = name
        self.description = description
        self.part_type_id = part_type_id
        self.color_id = color_id
        self.size_category_id = size_category_id

    def serialize(self):
        return {
            'id': self.id,
            'lego_item_number': self.lego_item_number,
            'name': self.name,
            'description': self.description,
            'part_type_id': self.part_type_id,
            'color_id': self.color_id,
            'size_category_id': self.size_category_id,
        }

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    floor_number = db.Column(db.Integer, nullable=False)

    def __init__(self, name, description, floor_number):
        self.name = name
        self.description = description
        self.floor_number = floor_number

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'floor_number': self.floor_number,
        }

class ShelvingUnit(db.Model):
    __tablename__ = 'shelving_units'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(256), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    number_of_shelves = db.Column(db.Integer, nullable=False)
    adjustable_shelves = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, description, location_id, number_of_shelves, adjustable_shelves):
        self.description = description
        self.location_id = location_id
        self.number_of_shelves = number_of_shelves
        self.adjustable_shelves = adjustable_shelves

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'location_id': self.location_id,
            'number_of_shelves': self.number_of_shelves,
            'adjustable_shelves': self.adjustable_shelves,
        }
class Shelf(db.Model):
    __tablename__ = 'shelves'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shelving_unit_id = db.Column(db.Integer, db.ForeignKey('shelving_units.id'), nullable=False)
    shelf_number = db.Column(db.Integer, nullable=False)

    def __init__(self, shelving_unit_id, shelf_number):
        self.shelving_unit_id = shelving_unit_id
        self.shelf_number = shelf_number

    def serialize(self):
        return {
            'id': self.id,
            'shelving_unit_id': self.shelving_unit_id,
            'shelf_number': self.shelf_number,
        }
class Container(db.Model):
    __tablename__ = 'containers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(256), nullable=True)
    shelf_id = db.Column(db.Integer, db.ForeignKey('shelves.id'), nullable=False)
    percentage_full = db.Column(db.Float, nullable=False, default=0.0)
    number_of_compartments = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, description, shelf_id, percentage_full, number_of_compartments):
        self.description = description
        self.shelf_id = shelf_id
        self.percentage_full = percentage_full
        self.number_of_compartments = number_of_compartments

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'shelf_id': self.shelf_id,
            'percentage_full': self.percentage_full,
            'number_of_compartments': self.number_of_compartments,
        }

class Compartment(db.Model):
    __tablename__ = 'compartments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    container_id = db.Column(db.Integer, db.ForeignKey('containers.id'), nullable=False)
    compartment_number = db.Column(db.Integer, nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('parts.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    percentage_full = db.Column(db.Float, nullable=False, default=0.0)

    def __init__(self, container_id, compartment_number, part_id, quantity, percentage_full):
        self.container_id = container_id
        self.compartment_number = compartment_number
        self.part_id = part_id
        self.quantity = quantity
        self.percentage_full = percentage_full

    def serialize(self):
        return {
            'id': self.id,
            'container_id': self.container_id,
            'compartment_number': self.compartment_number,
            'part_id': self.part_id,
            'quantity': self.quantity,
            'percentage_full': self.percentage_full,
        }