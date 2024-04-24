from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from app.models import Band, Event, Hotel, HotelReservation, Place, Contact, Contract, Function, Place, Invoice
from app.database import db
from app.utils import to_int_or_none

web = Blueprint('web', __name__)

# Routes for Bands
@web.route('/bands')
def list_bands():
    bands = Band.query.all()
    return render_template('bands/list.html', bands=bands)

@web.route('/bands/new', methods=['GET', 'POST'])
@web.route('/bands/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_band(id=None):
    band = Band.query.get(id) if id else Band()
    if request.method == 'POST':
        band.name = request.form.get('name', '')
        band.musicians_count = to_int_or_none(request.form.get('musicians_count'))
        band.techs_count = to_int_or_none(request.form.get('techs_count'))
        band.accomp_count = to_int_or_none(request.form.get('accomp_count'))
        band.tech_rider_url = request.form.get('tech_rider_url', '')
        db.session.add(band) if not band.id else None
        db.session.commit()
        flash('Band saved successfully!', 'success')
        return redirect(url_for('web.list_bands'))
    return render_template('bands/form.html', band=band)

@web.route('/bands/<int:id>/delete', methods=['POST'])
def delete_band(id):
    band = Band.query.get_or_404(id)
    db.session.delete(band)
    db.session.commit()
    flash('Band deleted successfully!', 'info')
    return redirect(url_for('web.list_bands'))

# Routes for Events
@web.route('/events')
def list_events():
    events = Event.query.all()
    return render_template('events/list.html', events=events)

@web.route('/events/new', methods=['GET', 'POST'])
@web.route('/events/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_event(id=None):
    event = Event.query.get(id) if id else Event()
    places = Place.query.all()
    bands = Band.query.all()

    if request.method == 'POST':
        event.title = request.form.get('title', '')
        event_date = request.form.get('date', '')
        event.place_id = request.form.get('place_id', '')

        try:
            event.date = datetime.strptime(event_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('events/form.html', event=event, places=places, bands=bands)

        band_ids = request.form.getlist('band_ids[]')
        if not band_ids:
            flash('At least one band must be selected.', 'error')
            return render_template('events/form.html', event=event, places=places, bands=bands)

        # Update the bands associated with the event
        event.bands = [Band.query.get(band_id) for band_id in band_ids if Band.query.get(band_id)]

        db.session.add(event)  # Add the event if it's new
        db.session.commit()
        flash('Event saved successfully!', 'success')
        return redirect(url_for('web.list_events'))

    # Prepare data for GET request
    event_date = event.date.strftime('%Y-%m-%d') if event.date else ''
    current_app.logger.info(f"Event date: {event_date}")
    event_band_ids = [band.id for band in event.bands] if event.bands else []

    return render_template('events/form.html', event=event, places=places, bands=bands, event_date=event_date, event_band_ids=event_band_ids)

@web.route('/events/<int:id>/delete', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'info')
    return redirect(url_for('web.list_events'))


# Routes for Functions
@web.route('/functions')
def list_functions():
    functions = Function.query.all()
    return render_template('functions/list.html', functions=functions)

@web.route('/functions/new', methods=['GET', 'POST'])
@web.route('/functions/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_function(id=None):
    function = Function.query.get(id) if id else Function()
    if request.method == 'POST':
        function.name = request.form.get('name')
        db.session.add(function) if not function.id else None
        db.session.commit()
        flash('Function saved successfully!', 'success')
        return redirect(url_for('web.list_functions'))
    return render_template('functions/form.html', function=function)

@web.route('/functions/<int:id>/delete', methods=['POST'])
def delete_function(id):
    function = Function.query.get_or_404(id)
    db.session.delete(function)
    db.session.commit()
    flash('Function deleted successfully!', 'info')
    return redirect(url_for('web.list_functions'))


# Routes for Hotels
@web.route('/hotels')
def list_hotels():
    hotels = Hotel.query.all()
    return render_template('hotels/list.html', hotels=hotels)

@web.route('/hotels/new', methods=['GET', 'POST'])
@web.route('/hotels/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_hotel(id=None):
    hotel = Hotel.query.get(id) if id else Hotel()
    if request.method == 'POST':
        hotel.name = request.form.get('name')
        hotel.address = request.form.get('address')
        hotel.email = request.form.get('email')
        hotel.phone = request.form.get('phone')
        db.session.add(hotel) if not hotel.id else None
        db.session.commit()
        flash('Hotel saved successfully!', 'success')
        return redirect(url_for('web.list_hotels'))
    return render_template('hotels/form.html', hotel=hotel)

@web.route('/hotels/<int:id>/delete', methods=['POST'])
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully!', 'info')
    return redirect(url_for('web.list_hotels'))

# Routes for Hotel Reservations
@web.route('/hotelReservations')
def list_hotel_reservations():
    reservations = HotelReservation.query.all()
    return render_template('hotelReservations/list.html', reservations=reservations)

@web.route('/hotelReservations/new', methods=['GET', 'POST'])
@web.route('/hotelReservations/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_hotel_reservation(id=None):
    reservation = HotelReservation.query.get(id) if id else HotelReservation()
    if request.method == 'POST':
        reservation.event_date = request.form.get('event_date')
        reservation.hotel_id = request.form.get('hotel_id')
        reservation.event_id = request.form.get('event_id')
        db.session.add(reservation) if not reservation.id else None
        db.session.commit()
        flash('Hotel Reservation saved successfully!', 'success')
        return redirect(url_for('web.list_hotel_reservations'))
    hotels = Hotel.query.all()
    events = Event.query.all()
    return render_template('hotelReservations/form.html', reservation=reservation, hotels=hotels, events=events)

@web.route('/hotelReservations/<int:id>/delete', methods=['POST'])
def delete_hotel_reservation(id):
    reservation = HotelReservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Hotel Reservation deleted successfully!', 'info')
    return redirect(url_for('web.list_hotel_reservations'))


# Routes for Contacts
@web.route('/contacts')
def list_contacts():
    contacts = Contact.query.all()
    return render_template('contacts/list.html', contacts=contacts)

@web.route('/contacts/new', methods=['GET', 'POST'])
@web.route('/contacts/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_contact(id=None):
    contact = Contact.query.get(id) if id else Contact()
    if request.method == 'POST':
        contact.name = request.form.get('name')
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.function_id = request.form.get('function_id')
        db.session.add(contact) if not contact.id else None
        db.session.commit()
        flash('Contact saved successfully!', 'success')
        return redirect(url_for('web.list_contacts'))
    functions = Function.query.all()
    return render_template('contacts/form.html', contact=contact, functions=functions)

@web.route('/contacts/<int:id>/delete', methods=['POST'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'info')
    return redirect(url_for('web.list_contacts'))

# Routes for Contracts
@web.route('/contracts')
def list_contracts():
    contracts = Contract.query.all()
    return render_template('contracts/list.html', contracts=contracts)

@web.route('/contracts/new', methods=['GET', 'POST'])
@web.route('/contracts/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_contract(id=None):
    contract = Contract.query.get(id) if id else Contract()

    if request.method == 'POST':
        contract.name = request.form.get('name')
        contract.start_date = request.form.get('start_date')
        contract.end_date = request.form.get('end_date')
        contract.band_id = request.form.get('band_id')
        db.session.add(contract) if not contract.id else None
        db.session.commit()
        flash('Contract saved successfully!', 'success')
        return redirect(url_for('web.list_contracts'))
    bands = Band.query.all()
    return render_template('contracts/form.html', contract=contract, bands=bands)

@web.route('/contracts/<int:id>/delete', methods=['POST'])
def delete_contract(id):
    contract = Contract.query.get_or_404(id)
    db.session.delete(contract)
    db.session.commit()
    flash('Contract deleted successfully!', 'info')
    return redirect(url_for('web.list_contracts'))

# Routes for Places
@web.route('/places')
def list_places():
    places = Place.query.all()
    return render_template('places/list.html', places=places)

@web.route('/places/new', methods=['GET', 'POST'])
@web.route('/places/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_place(id=None):
    place = Place.query.get(id) if id else Place()
    if request.method == 'POST':
        place.name = request.form.get('name')
        place.address = request.form.get('address')
        place.email = request.form.get('email')
        place.phone = request.form.get('phone')
        db.session.add(place) if not place.id else None
        db.session.commit()
        flash('Place saved successfully!', 'success')
        return redirect(url_for('web.list_places'))
    return render_template('places/form.html', place=place)

@web.route('/places/<int:id>/delete', methods=['POST'])
def delete_place(id):
    place = Place.query.get_or_404(id)
    db.session.delete(place)
    db.session.commit()
    flash('Place deleted successfully!', 'info')
    return redirect(url_for('web.list_places'))


# Routes for Invoices
@web.route('/invoices')
def list_invoices():
    invoices = Invoice.query.all()
    return render_template('invoices/list.html', invoices=invoices)

@web.route('/invoices/new', methods=['GET', 'POST'])
@web.route('/invoices/<int:id>/edit', methods=['GET', 'POST'])
def create_or_edit_invoice(id=None):
    invoice = Invoice.query.get(id) if id else Invoice()
    if request.method == 'POST':
        invoice.amount = float(request.form.get('amount'))
        invoice.date = request.form.get('date')
        invoice.event_id = request.form.get('event_id')
        db.session.add(invoice) if not invoice.id else None
        db.session.commit()
        flash('Invoice saved successfully!', 'success')
        return redirect(url_for('web.list_invoices'))
    events = Event.query.all()
    return render_template('invoices/form.html', invoice=invoice, events=events)

@web.route('/invoices/<int:id>/delete', methods=['POST'])
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    db.session.commit()
    flash('Invoice deleted successfully!', 'info')
    return redirect(url_for('web.list_invoices'))

# Further entities like Hotels, Hotel Reservations, Contacts, etc. should follow similar patterns:
# - Define routes for listing items
# - Define routes for new item creation and editing
# - Handle POST requests within those routes to update the database
# - Provide feedback to the user with flash messages
# - Redirect to the listing page after actions

# Make sure to add routes for deletion with confirmation for all entities
