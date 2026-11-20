# API for compartments table
from flask import Blueprint, jsonify, request, abort
from ..models import db, Compartment
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('compartments', __name__, url_prefix='/compartments')

@bp.route('', methods=['GET'])
def index():
    compartments = Compartment.query.all()
    result = []
    for c in compartments:
        result.append(c.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    compartment = Compartment.query.get_or_404(id)
    return jsonify(compartment.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain container_id, compartment_number, part_id, quantity, percentage_full
    if 'container_id' not in request.json or 'compartment_number' not in request.json or 'part_id' not in request.json or 'quantity' not in request.json or 'percentage_full' not in request.json:
        return abort(400)
    
    # construct Compartment
    c = Compartment(
        container_id=request.json['container_id'],
        compartment_number=request.json['compartment_number'],
        part_id=request.json['part_id'],
        quantity=request.json['quantity'],
        percentage_full=request.json['percentage_full']
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())

