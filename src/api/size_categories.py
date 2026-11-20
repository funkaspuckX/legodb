# API for size_categories table
from flask import Blueprint, jsonify, request, abort
from ..models import db, SizeCategory
import hashlib
import secrets
import sqlalchemy

bp = Blueprint('size_categories', __name__, url_prefix='/size_categories')

@bp.route('', methods=['GET'])
def index():
    size_categories = SizeCategory.query.all()
    result = []
    for sc in size_categories:
        result.append(sc.serialize())
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    size_category = SizeCategory.query.get_or_404(id)
    return jsonify(size_category.serialize()), 200

@bp.route('', methods=['POST'])
def create():
    # req body must contain name, description
    if 'name' not in request.json or 'description' not in request.json:
        return abort(400)
    
    # construct SizeCategory
    sc = SizeCategory(
        name=request.json['name'],
        description=request.json['description']
    )
    db.session.add(sc) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(sc.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    sc = SizeCategory.query.get_or_404(id)
    try:
        db.session.delete(sc) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

    