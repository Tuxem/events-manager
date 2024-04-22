from flask import Blueprint, request, jsonify
from app.models.models import db, Hotel, HotelReservation, Event, Band, Contact, Contract, Function, Place, Invoice, Configuration

bp = Blueprint('api', __name__, url_prefix='/api')

# Helper function to serialize model instances
def serialize(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

# Helper to serialize list of models
def serialize_list(items):
    return [serialize(item) for item in items]

# CRUD Routes for Hotels
@bp.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify(serialize_list(hotels))

@bp.route('/hotels', methods=['POST'])
def create_hotel():
    data = request.get_json()
    hotel = Hotel(address=data['address'], phone=data['phone'], email=data['email'])
    db.session.add(hotel)
    db.session.commit()
    return jsonify(serialize(hotel)), 201

@bp.route('/hotels/<int:id>', methods=['PUT'])
def update_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    data = request.get_json()
    hotel.address = data.get('address', hotel.address)
    hotel.phone = data.get('phone', hotel.phone)
    hotel.email = data.get('email', hotel.email)
    db.session.commit()
    return jsonify(serialize(hotel))

@bp.route('/hotels/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({'message': 'Hotel deleted'}), 204

# CRUD Routes for Hotel Reservations
@bp.route('/hotel_reservations', methods=['GET'])
def get_hotel_reservations():
    reservations = HotelReservation.query.all()
    return jsonify(serialize_list(reservations))

@bp.route('/hotel_reservations', methods=['POST'])
def create_hotel_reservation():
    data = request.get_json()
    reservation = HotelReservation(
        event_date=data['event_date'],
        hotel_id=data['hotel_id'],
        event_id=data['event_id']
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify(serialize(reservation)), 201

@bp.route('/hotel_reservations/<int:id>', methods=['PUT'])
def update_hotel_reservation(id):
    reservation = HotelReservation.query.get_or_404(id)
    data = request.get_json()
    reservation.event_date = data.get('event_date', reservation.event_date)
    reservation.hotel_id = data.get('hotel_id', reservation.hotel_id)
    reservation.event_id = data.get('event_id', reservation.event_id)
    db.session.commit()
    return jsonify(serialize(reservation))

@bp.route('/hotel_reservations/<int:id>', methods=['DELETE'])
def delete_hotel_reservation(id):
    reservation = HotelReservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({'message': 'Hotel Reservation deleted'}), 204

# CRUD Routes for Events
@bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify(serialize_list(events))

@bp.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    event = Event(
        date=data['date'],
        place_id=data['place_id']
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(serialize(event)), 201

@bp.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    event.date = data.get('date', event.date)
    event.place_id = data.get('place_id', event.place_id)
    db.session.commit()
    return jsonify(serialize(event))

@bp.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 204

# Example CRUD for Band
@bp.route('/bands', methods=['GET'])
def get_bands():
    bands = Band.query.all()
    return jsonify(serialize_list(bands))

@bp.route('/bands', methods=['POST'])
def create_band():
    data = request.get_json()
    band = Band(
        name=data['name'],
        musicians_count=data['musicians_count'],
        techs_count=data['techs_count'],
        accomp_count=data['accomp_count'],
        tech_rider_url=data['tech_rider_url']
    )
    db.session.add(band)
    db.session.commit()
    return jsonify(serialize(band)), 201

@bp.route('/bands/<int:id>', methods=['PUT'])
def update_band(id):
    band = Band.query.get_or_404(id)
    data = request.get_json()
    band.name = data.get('name', band.name)
    band.musicians_count = data.get('musicians_count', band.musicians_count)
    band.techs_count = data.get('techs_count', band.techs_count)
    band.accomp_count = data.get('accomp_count', band.accomp_count)
    band.tech_rider_url = data.get('tech_rider_url', band.tech_rider_url)
    db.session.commit()
    return jsonify(serialize(band))

@bp.route('/bands/<int:id>', methods=['DELETE'])
def delete_band(id):
    band = Band.query.get_or_404(id)
    db.session.delete(band)
    db.session.commit()
    return jsonify({'message': 'Band deleted'}), 204

