# API for locations table
from flask import Blueprint, jsonify, request, abort
from ..models import db, Location
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('locations', __name__, url_prefix='/locations')

@bp.route('', methods=['GET'])
def index():
    locations = Location.query.all()
    result = []
    for l in locations:
        result.append(l.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    location = Location.query.get_or_404(id)
    return jsonify(location.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain name, description, and floor_number
    if 'name' not in request.json or 'description' not in request.json or 'floor_number' not in request.json:
        return abort(400)
    
    # construct Location
    l = Location(
        name=request.json['name'],
        description=request.json['description'],
        floor_number=request.json['floor_number']
    )
    db.session.add(l) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(l.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    l = Location.query.get_or_404(id)
    try:
        db.session.delete(l) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    