# API for part_types table
from flask import Blueprint, jsonify, request, abort
from ..models import db, PartType
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('part_types', __name__, url_prefix='/part_types')

@bp.route('', methods=['GET'])
def index():
    part_types = PartType.query.all()
    result = []
    for pt in part_types:
        result.append(pt.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    part_type = PartType.query.get_or_404(id)
    return jsonify(part_type.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain name, description
    if 'name' not in request.json or 'description' not in request.json:
        return abort(400)
    
    # construct PartType
    pt = PartType(
        name=request.json['name'],
        description=request.json['description']
    )
    db.session.add(pt) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(pt.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    pt = PartType.query.get_or_404(id)
    try:
        db.session.delete(pt) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    