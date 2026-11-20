# a report API showing contents of a location, including the parts in the room and their quantities
from flask import Blueprint, jsonify, request, abort
from sqlalchemy import text
from ..models import db, Location, Shelf, Container, Compartment, Part, ShelvingUnit

bp = Blueprint('room_inventory_report', __name__, url_prefix='/room_inventory_report')

#debug test route
@bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Room Inventory Report API is working!"}), 200

@bp.route('/<int:location_id>', methods=['GET'])
def show(location_id: int):
    location = Location.query.get_or_404(location_id)
    # Implementation for showing location inventory report from raw sql
    sql = text("""
        SELECT 
       l.id AS location_id,
       l.name AS location_name,
	   s.id AS shelf_id,
	   s.shelf_number AS shelf_number,
	   su.id AS shelving_unit_id,
	   su.description AS shelving_unit_description,
	   cr.id AS container_id,
	   cr.description AS container_description,
	   c.id AS compartment_id,
	   c.compartment_number AS compartment_number,
	   p.id AS part_id,
	   p.name AS part_name
 FROM parts p
 JOIN compartments c ON c.part_id = part_id
 JOIN containers cr ON cr.id = c.container_id
 JOIN shelves s ON s.id = cr.shelf_id
 JOIN shelving_units su ON su.id = s.shelving_unit_id
 JOIN locations l ON l.id = su.location_id
        WHERE l.id = :location_id
    """)
    
    result = db.session.execute(sql, {"location_id": location_id}).all()
    report = []
    for row in result:
        report.append({
            'location_id': row.location_id,
            'location_name': row.location_name,
            'shelf_id': row.shelf_id,
            'shelf_number': row.shelf_number,
            'shelving_unit_id': row.shelving_unit_id,
            'shelving_unit_description': row.shelving_unit_description,
            'container_id': row.container_id,
            'container_description': row.container_description,
            'compartment_id': row.compartment_id,
            'compartment_number': row.compartment_number,
            'part_id': row.part_id,
            'part_name': row.part_name
            
        })
    return jsonify(report), 200 
