# API for containers table
from flask import Blueprint, jsonify, request, abort
from ..models import db, Container
import hashlib
import secrets
import sqlalchemy   

bp = Blueprint('containers', __name__, url_prefix='/containers')

@bp.route('', methods=['GET'])
def index():
    containers = Container.query.all()
    result = []
    for c in containers:
        result.append(c.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    container = Container.query.get_or_404(id)
    return jsonify(container.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain description, shelf_id, percentage_full, number_of_parts, and location_id
    if 'description' not in request.json or 'shelf_id' not in request.json or 'percentage_full' not in request.json or 'number_of_compartments' not in request.json :
        return abort(400)
    
    # construct Container
    c = Container(
        description=request.json['description'],
        shelf_id=request.json['shelf_id'],
        percentage_full=request.json['percentage_full'],
        number_of_compartments=request.json['number_of_compartments'] 
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Container.query.get_or_404(id)
    try:
        db.session.delete(c) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
    