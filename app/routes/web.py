from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SelectMultipleField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired
from sqlalchemy.exc import SQLAlchemyError

from app.models import EventBand, Band, Event, Hotel, HotelReservation, Place, Contact, Contract, Function, Place, Invoice
from app.database import db
from app.utils import to_int_or_none

web = Blueprint('web', __name__)


class EventForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    place_id = SelectField('Place', coerce=int, validators=[DataRequired()])
    band_ids = SelectMultipleField('Bands', coerce=int)

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
    """
    Handle creation and editing of events.

    If an ID is provided, the function will fetch the event for editing.
    Without an ID, the function prepares to create a new event.

    Args:
        id (int, optional): The ID of the event to edit. Defaults to None for creating a new event.

    Returns:
        render_template: Renders the 'events/form.html' template with event data and band information.
        redirect: Redirects to the list of events on successful creation or update.
    """
    try:
        event = Event.query.get(id) if id else Event()
        form = EventForm(obj=event)
        places = Place.query.all()
        bands = Band.query.order_by(Band.name).all()  # Assuming Band has a column 'name'
        event_date = event.date.strftime('%Y-%m-%d') if event.date else ''


        # Fetching bands associated with the event and their order
        event_bands = EventBand.query.filter_by(event_id=id).order_by(EventBand.order.asc()).all()
        event_band_ids = [eb.band_id for eb in event_bands]

        if request.method == 'POST':
            event_date = request.form['date']
            place_id = request.form['place_id']
            band_ids = request.form.getlist('band_ids[]')
            band_order = request.form.getlist('band_order[]')

            event.date = datetime.strptime(event_date, '%Y-%m-%d') if event_date else None
            event.place_id = place_id

            if not event.id:
                db.session.add(event)
            db.session.flush()  # Flush to assign an ID to the new event

            EventBand.query.filter_by(event_id=event.id).delete()
            db.session.flush()  # Ensure deletions are processed

            for index, band_id in enumerate(band_ids):
                order = int(band_order[index]) if index < len(band_order) else len(band_ids) - index
                new_event_band = EventBand(event_id=event.id, band_id=int(band_id), order=order)
                db.session.add(new_event_band)

            db.session.commit()
            flash('Event updated successfully!' if id else 'Event created successfully!')
            return redirect(url_for('web.list_events'))

        return render_template(
            'events/form.html',
            event=event,
            places=places,
            bands=bands,
            event_bands=event_bands,
            form=form,
            event_date=event_date
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error('Database error occurred', exc_info=e)
        flash('Database error occurred. Please try again.', 'error')
        return render_template(
            'events/form.html',
            event=event,
            places=places,
            bands=bands
        ), 500
    except Exception as e:
        current_app.logger.error('An error occurred', exc_info=e)
        flash('An error occurred. Please try again.', 'error')
        return render_template(
            'events/form.html',
            event=event,
            places=places,
            bands=bands
        ), 500


@web.route('/events/<int:id>/delete', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    EventBand.query.filter_by(event_id=id).delete()  # Explicitly delete EventBand associations
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
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
