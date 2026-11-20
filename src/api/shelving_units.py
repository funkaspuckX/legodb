# API for shelving_units table
from flask import Blueprint, jsonify, request, abort
from ..models import db, ShelvingUnit
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('shelving_units', __name__, url_prefix='/shelving_units')

@bp.route('', methods=['GET'])
def index():
    shelving_units = ShelvingUnit.query.all()
    result = []
    for su in shelving_units:
        result.append(su.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    shelving_unit = ShelvingUnit.query.get_or_404(id)
    return jsonify(shelving_unit.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain description, location_id, number_of_shelves and adjustable_shelves
    if 'description' not in request.json or 'location_id' not in request.json or 'number_of_shelves' not in request.json or 'adjustable_shelves' not in request.json:
        return abort(400)
    
    # construct ShelvingUnit
    su = ShelvingUnit(
        description=request.json['description'],
        location_id=request.json['location_id'],
        number_of_shelves=request.json['number_of_shelves'],
        adjustable_shelves=request.json['adjustable_shelves']
    )
    db.session.add(su) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(su.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    su = ShelvingUnit.query.get_or_404(id)
    try:
        db.session.delete(su) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    