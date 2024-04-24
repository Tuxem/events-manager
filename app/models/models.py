from flask_sqlalchemy import SQLAlchemy

from app import db

# New models should be added to the import statement in app/models/__init__.py

class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    reservations = db.relationship('HotelReservation', back_populates='hotel')

class HotelReservation(db.Model):
    __tablename__ = 'hotel_reservation'
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.DateTime)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    hotel = db.relationship('Hotel', back_populates='reservations')
    event = db.relationship('Event', back_populates='hotel_reservations')

class EventBand(db.Model):
    __tablename__ = 'event_bands'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'), primary_key=True)
    order = db.Column(db.Integer)  # This column will store the order of bands
    
    # Relationship to Event and Band
    event = db.relationship("Event", back_populates="bands")
    band = db.relationship("Band", back_populates="events")

class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    musicians_count = db.Column(db.Integer)
    techs_count = db.Column(db.Integer)
    accomp_count = db.Column(db.Integer)
    tech_rider_url = db.Column(db.String)
    events = db.relationship('EventBand', back_populates='band', order_by=EventBand.order)
    contracts = db.relationship('Contract', back_populates='band')

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String, nullable=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    hotel_reservations = db.relationship('HotelReservation', back_populates='event')
    place = db.relationship('Place', back_populates='events')
    bands = db.relationship('EventBand', back_populates='event', order_by=EventBand.order)
    contracts = db.relationship('Contract', back_populates='associated_event')

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    function_id = db.Column(db.Integer, db.ForeignKey('function.id'))
    function = db.relationship('Function', back_populates='contacts')

class Contract(db.Model):
    __tablename__ = 'contract'
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    band = db.relationship('Band', back_populates='contracts')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    associated_event = db.relationship('Event', back_populates='contracts')
    invoices = db.relationship('Invoice', back_populates='contract', lazy='dynamic')

class Function(db.Model):
    __tablename__ = 'function'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    contacts = db.relationship('Contact', back_populates='function')

class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    events = db.relationship('Event', back_populates='place')

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    invoice_url = db.Column(db.String)
    paid = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime)
    issue_date = db.Column(db.DateTime)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))

    # Relationship: One Invoice to One Contract
    contract = db.relationship('Contract', back_populates='invoices', uselist=False)

class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
