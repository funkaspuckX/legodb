# API for shelves table
from flask import Blueprint, jsonify, request, abort
from ..models import db, Shelf
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('shelves', __name__, url_prefix='/shelves')

@bp.route('', methods=['GET'])
def index():
    shelves = Shelf.query.all()
    result = []
    for s in shelves:
        result.append(s.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    shelf = Shelf.query.get_or_404(id)
    return jsonify(shelf.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain shelving_unit_id and shelf_number
    if 'shelving_unit_id' not in request.json or 'shelf_number' not in request.json:
        return abort(400)
    
    # construct Shelf
    s = Shelf(
        shelving_unit_id=request.json['shelving_unit_id'],
        shelf_number=request.json['shelf_number']
    )
    db.session.add(s) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(s.serialize())   

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    s = Shelf.query.get_or_404(id)
    try:
        db.session.delete(s) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    