# API for parts table
from flask import Blueprint, jsonify, request, abort
from ..models import Part, db
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('parts', __name__, url_prefix='/parts')

@bp.route('', methods=['GET'])
def index():
    parts = Part.query.all()
    result = []
    for p in parts:
        result.append(p.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    part = Part.query.get_or_404(id)
    return jsonify(part.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain name, description, part_type_id, color_id, size_category_id
    if 'name' not in request.json or 'description' not in request.json or 'part_type_id' not in request.json or 'color_id' not in request.json or 'size_category_id' not in request.json:
        return abort(400)
    
    # construct Part
    p = Part(
        name=request.json['name'],
        description=request.json['description'],
        part_type_id=request.json['part_type_id'],
        color_id=request.json['color_id'],
        size_category_id=request.json['size_category_id'],
        lego_item_number=request.json['lego_item_number']
    )
    db.session.add(p) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(p.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Part.query.get_or_404(id)
    try:
        db.session.delete(p) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)