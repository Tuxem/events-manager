from app import db

class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    email = db.Column(db.String)

class HotelReservation(db.Model):
    __tablename__ = 'hotel_reservation'
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.DateTime)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    hotel = db.relationship('Hotel', backref='reservations')
    event = db.relationship('Event', backref='hotel_reservations')

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    bands = db.relationship('Band', secondary='event_bands', backref=db.backref('events', lazy='dynamic'))
    contracts = db.relationship('Contract', backref='event', lazy='dynamic')
    place = db.relationship('Place', backref='events')

class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    musicians_count = db.Column(db.Integer)
    techs_count = db.Column(db.Integer)
    accomp_count = db.Column(db.Integer)
    tech_rider_url = db.Column(db.String)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    function_id = db.Column(db.Integer, db.ForeignKey('function.id'))
    function = db.relationship('Function', backref='contacts')

class Contract(db.Model):
    __tablename__ = 'contract'
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    band = db.relationship('Band', backref='contracts')

class Function(db.Model):
    __tablename__ = 'function'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    contacts = db.relationship('Contact', backref='function')

class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    invoice_url = db.Column(db.String)
    paid = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime)
    issue_date = db.Column(db.DateTime)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    contract = db.relationship('Contract', backref='invoices')
    band = db.relationship('Band', backref='invoices')

class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
