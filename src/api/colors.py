# API for colors table
from flask import Blueprint, jsonify, request, abort
from ..models import db, Color, Part
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('colors', __name__, url_prefix='/colors')

@bp.route('', methods=['GET'])
def index():
    colors = Color.query.all()
    result = []
    for c in colors:
        result.append(c.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    color = Color.query.get_or_404(id)
    return jsonify(color.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain name, hex_value
    if 'name' not in request.json or 'hex_value' not in request.json:
        return abort(400)
    
    # construct Color
    c = Color   (
        name=request.json['name'],
        hex_value=request.json['hex_value']
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Color.query.get_or_404(id)
    try:
        db.session.delete(c) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)