from flask import Blueprint, request, jsonify, abort
from sqlalchemy.inspection import inspect


from app.database import db
from app.models import Event, Band, Hotel, HotelReservation, Contact, Contract, Function, Place, Invoice, Configuration

api = Blueprint('api', __name__)

# Event Routes
@api.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200

@api.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(**data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

@api.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    db.session.commit()
    return jsonify(event.to_dict()), 200

@api.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Band Routes
@api.route('/bands', methods=['GET'])
def get_bands():
    query = request.args.get('query')
    if query:
        bands = Band.query.filter(Band.name.ilike(f'%{query}%')).all()
    else:
        bands = Band.query.all()
    return jsonify([band.to_dict() for band in bands]), 200

@api.route('/bands', methods=['POST'])
def create_band():
    data = request.get_json()
    new_band = Band(**data)
    db.session.add(new_band)
    db.session.commit()
    return jsonify(new_band.to_dict()), 201

@api.route('/bands/<int:id>', methods=['PUT'])
def update_band(id):
    band = Band.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(band, key, value)
    db.session.commit()
    return jsonify(band.to_dict()), 200

@api.route('/bands/<int:id>', methods=['DELETE'])
def delete_band(id):
    band = Band.query.get_or_404(id)
    db.session.delete(band)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Hotel Routes
@api.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify([model_to_dict(hotel) for hotel in hotels]), 200

@api.route('/hotels', methods=['POST'])
def create_hotel():
    data = request.get_json()
    new_hotel = Hotel(**data)
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify(model_to_dict(new_hotel)), 201

@api.route('/hotels/<int:id>', methods=['PUT'])
def update_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(hotel, key, value)
    db.session.commit()
    return jsonify(model_to_dict(hotel)), 200

@api.route('/hotels/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# HotelReservation Routes
@api.route('/hotel_reservations', methods=['GET'])
def get_hotel_reservations():
    reservations = HotelReservation.query.all()
    return jsonify([model_to_dict(reservation) for reservation in reservations]), 200

@api.route('/hotel_reservations', methods=['POST'])
def create_hotel_reservation():
    data = request.get_json()
    new_reservation = HotelReservation(**data)
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify(model_to_dict(new_reservation)), 201

@api.route('/hotel_reservations/<int:id>', methods=['PUT'])
def update_hotel_reservation(id):
    reservation = HotelReservation.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(reservation, key, value)
    db.session.commit()
    return jsonify(model_to_dict(reservation)), 200

@api.route('/hotel_reservations/<int:id>', methods=['DELETE'])
def delete_hotel_reservation(id):
    reservation = HotelReservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Contact Routes
@api.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([model_to_dict(contact) for contact in contacts]), 200

@api.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    new_contact = Contact(**data)
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(model_to_dict(new_contact)), 201

@api.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(contact, key, value)
    db.session.commit()
    return jsonify(model_to_dict(contact)), 200

@api.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Contract Routes
@api.route('/contracts', methods=['GET'])
def get_contracts():
    contracts = Contract.query.all()
    return jsonify([model_to_dict(contract) for contract in contracts]), 200

@api.route('/contracts', methods=['POST'])
def create_contract():
    data = request.get_json()
    new_contract = Contract(**data)
    db.session.add(new_contract)
    db.session.commit()
    return jsonify(model_to_dict(new_contract)), 201

@api.route('/contracts/<int:id>', methods=['PUT'])
def update_contract(id):
    contract = Contract.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(contract, key, value)
    db.session.commit()
    return jsonify(model_to_dict(contract)), 200

@api.route('/contracts/<int:id>', methods=['DELETE'])
def delete_contract(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Function Routes
@api.route('/functions', methods=['GET'])
def get_functions():
    functions = Function.query.all()
    return jsonify([model_to_dict(function) for function in functions]), 200

@api.route('/functions', methods=['POST'])
def create_function():
    data = request.get_json()
    new_function = Function(**data)
    db.session.add(new_function)
    db.session.commit()
    return jsonify(model_to_dict(new_function)), 201

@api.route('/functions/<int:id>', methods=['PUT'])
def update_function(id):
    function = Function.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(function, key, value)
    db.session.commit()
    return jsonify(model_to_dict(function)), 200

@api.route('/functions/<int:id>', methods=['DELETE'])
def delete_function(id):
    function = Function.query.get_or_404(id)
    db.session.delete(function)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Place Routes
@api.route('/places', methods=['GET'])
def get_places():
    places = Place.query.all()
    return jsonify([model_to_dict(place) for place in places]), 200

@api.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    new_place = Place(**data)
    db.session.add(new_place)
    db.session.commit()
    return jsonify(model_to_dict(new_place)), 201

@api.route('/places/<int:id>', methods=['PUT'])
def update_place(id):
    place = Place.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(place, key, value)
    db.session.commit()
    return jsonify(model_to_dict(place)), 200

@api.route('/places/<int:id>', methods=['DELETE'])
def delete_place(id):
    place = Place.query.get_or_404(id)
    db.session.delete(place)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Invoice Routes
@api.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([model_to_dict(invoice) for invoice in invoices]), 200

@api.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.get_json()
    new_invoice = Invoice(**data)
    db.session.add(new_invoice)
    db.session.commit()
    return jsonify(model_to_dict(new_invoice)), 201

@api.route('/invoices/<int:id>', methods=['PUT'])
def update_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(invoice, key, value)
    db.session.commit()
    return jsonify(model_to_dict(invoice)), 200

@api.route('/invoices/<int:id>', methods=['DELETE'])
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Configuration Routes
@api.route('/configurations', methods=['GET'])
def get_configurations():
    configurations = Configuration.query.all()
    return jsonify([model_to_dict(configuration) for configuration in configurations]), 200

@api.route('/configurations', methods=['POST'])
def create_configuration():
    data = request.get_json()
    new_configuration = Configuration(**data)
    db.session.add(new_configuration)
    db.session.commit()
    return jsonify(model_to_dict(new_configuration)), 201

@api.route('/configurations/<int:id>', methods=['PUT'])
def update_configuration(id):
    configuration = Configuration.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(configuration, key, value)
    db.session.commit()
    return jsonify(model_to_dict(configuration)), 200

@api.route('/configurations/<int:id>', methods=['DELETE'])
def delete_configuration(id):
    configuration = Configuration.query.get_or_404(id)
    db.session.delete(configuration)
    db.session.commit()
    return jsonify({'message': 'deleted'}), 200

# Utility function to convert model instances to dictionaries
def model_to_dict(instance, include_relationships=False):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(instance.__class__).columns]
    data = {c: getattr(instance, c) for c in columns}
    if include_relationships:
        relationships = class_mapper(instance.__class__).relationships.keys()
        for relationship in relationships:
            # Only include if you explicitly handle the serialization logic for relationships
            related_data = getattr(instance, relationship)
            if related_data:
                if hasattr(related_data, 'to_dict'):
                    data[relationship] = related_data.to_dict()  # Recursive to_dict
                else:
                    data[relationship] = str(related_data)  # Or handle as a string or in a suitable format
    return data

