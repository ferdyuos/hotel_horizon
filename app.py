from datetime import datetime
import json
import os
from pathlib import Path
from flask import Flask, current_app, jsonify, render_template, request, send_file, send_from_directory, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user
from idna import decode
from constants import BASE_DIR
from utilities.tools import create_hashid, _SECRET_KEY, decode_hashid, get_cancel_charge, get_discount_rate, get_peak_season, get_prices, get_ref_code, get_room_details, render_to_pdf
from models.my_models import Booking, BookingStatusEnum, Hotel, RoomTypeEnum, SeasonTypeEnum, User, db
from forms import HotelForm, LoginForm, RegistrationForm
from flask_login import LoginManager, login_user, current_user
from flask_cors import CORS
from flask_basicauth import BasicAuth
import dateutil.parser

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['SECRET_KEY'] = _SECRET_KEY # creates a secret key for the app to manage user sessions
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///test.db' # config for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basic_auth = BasicAuth(app)
app.jinja_env.globals.update(create_hashid=create_hashid)

# init database
db.init_app(app)
with app.app_context():
    db.create_all()

# login management
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/api/login/', methods=['POST'])
@basic_auth.required
def api_login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is not None and user.check_password(data['password']):
        login_user(user)
        next = request.args.get("next")
        return jsonify({'status': 'Ok.', 'id': create_hashid(user.id)})
    return jsonify({'error': 'Invalid email address or Password.'})


@app.route('/api/register/', methods=['POST'])
@basic_auth.required
def api_register():
    data = request.get_json() if request.get_json() != None else request.get_data()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        try:
            user = User(username=data['username'], staff=False, email=data['email'])
            user.set_password(data['password'])
            print(user)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message":"User created", "id":create_hashid(user.id)})
        except Exception as e:
            print(e)
            return jsonify({'error': 'An error occured while creating user'})
    return jsonify({'error':'User Already Registered'})


# @login_required
@app.route("/api/logout/")
@basic_auth.required
def api_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/api/change-info/', methods=['POST'])
@basic_auth.required
# @login_required
def api_change_info():
    data = request.get_json()
    id = decode_hashid(data['id'])
    user = User.query.get_or_404(id=id)
    user.username = data['username']
    user.set_password(data['password'])
    try:
        db.session.commit()
        return jsonify({'status':'ok'})
    except Exception as e:
        return jsonify({'error':'Error occured while updating user info'})



@app.route('/api/hotel-listings/')
@basic_auth.required
# @login_required
def hotel_listings():
    hotels = Hotel.query.order_by(Hotel.date).all()
    hotel_list = [ {'id':create_hashid(hotel.id), 'city': hotel.city, 'capacity':hotel.capacity, 'peak_rate':hotel.peak_rate,
     'off_peak_rate':hotel.off_peak_rate, 'description':hotel.description}
     for hotel in hotels
    ]
    # return render_template('hotel_list.html', hotels=hotels)
    return jsonify(hotel_list)

@app.route('/api/book/', methods=['POST'])
@basic_auth.required
# @login_required
def make_booking():
    """{ id, type, date, number_people }"""
    info = request.get_json()
    id = info['id']
    id = decode_hashid(id)[0]
    print(id)
    hotel = Hotel.query.get_or_404(id)
    type = info['type']
    prices = get_prices(hotel)
    room_type = RoomTypeEnum.standard
    user_id = decode_hashid(info['user_id'])[0]
    amount_payable = 0
    season = get_peak_season()
    if type == 'standard':
        amount_payable = prices['s_peak'] if season == 'peak' else prices['s_off_peak']
    elif type == 'double':
        room_type = RoomTypeEnum.double
        amount_payable = prices['d_peak'] if season == 'peak' else prices['d_off_peak']
    else:
        room_type = RoomTypeEnum.family
        amount_payable = prices['f_peak'] if season == 'peak' else prices['f_off_peak']
    
    date = info['date']
    date = dateutil.parser.parse(date)
    number_people = info['number_people']
    
    if room_type == RoomTypeEnum.double and number_people == 2:
        amount_payable += amount_payable * 0.1
    s = SeasonTypeEnum.peak if season == 'peak' else SeasonTypeEnum.off_peak

    booking = Booking(user_id=user_id, hotel_id=id,
    season=s, 
    status=BookingStatusEnum.not_paid, ref_code=get_ref_code(15),
    room_type=room_type, date=date, number_people=number_people, amount=amount_payable)

    discount_details = get_discount_rate(booking, amount_payable)
    amount_payable = discount_details['to_pay']
    booking.amount = amount_payable

    try:
        db.session.add(booking)

        db.session.commit()
        # pdf = render_to_pdf({'booking': booking, 'user':User.query.get(user_id)})
        return jsonify({'ref_code':booking.ref_code, 'amount':booking.amount, 'id':create_hashid(booking.id)})
    except Exception as e:
        print(e)
        return jsonify({'error': "An error occurred while booking your room"})


@app.route('/api/payment/', methods=['POST'])
@basic_auth.required
def payment():
    """booking_id, user_id"""
    info = request.get_json()
    booking_id = decode_hashid(info.get('booking_id'))[0]
    user_id = decode(info.get('user_id'))
    booking = Booking.query.get(booking_id)
    booking.status= BookingStatusEnum.paid
    db.session.commit()
    pdf = render_to_pdf({'booking': booking, 'user':User.query.get(user_id)})
    return jsonify(pdf)


@app.route("/api/download/ticket/")
def tos():
    filepath = BASE_DIR /"documents/"
    return send_from_directory(filepath, 'ticket.pdf')



@app.route('/api/my-bookings/', methods=['POST'])
@basic_auth.required
# @login_required   
def api_my_bookings():
    info = request.get_json()
    id = decode_hashid(info['id'])[0]
    bookings = Booking.query.filter_by(user_id=id).all()
    booking_list = [
        {'id': create_hashid(booking.id), 'city':booking.hotel.city, 'ref_code':booking.ref_code, 'status':booking.status.value}
        for booking in bookings
    ]
    return jsonify(booking_list)


@app.route('/api/cancel-booking/', methods=['POST'])
@basic_auth.required
# @login_required
def api_cancel_booking():
    data = request.get_json()
    id = decode_hashid(data['id'])
    booking = Booking.query.get_or_404(id)
    if booking.status == BookingStatusEnum.not_paid:
        try:
            # Booking.delete(booking)
            db.session.delete(booking)
            db.session.commit()
            return jsonify({"status":"Deleted"})
        except Exception as e:
            print(e)
            return jsonify({"error":"An error occured while deleting booking"})
    else:
        charge = get_cancel_charge(booking)
        if charge == 0:
            booking.status = BookingStatusEnum.cancelled
            try:
                db.session.commit()
                return jsonify({'status':'ok'})
            except Exception:
                return "An error occurred while updating your task."
        else:
            booking.status = BookingStatusEnum.cancelled
            booking.cancel_charge = charge
            try:
                db.session.commit()
                return jsonify({'status': 'ok', 'message':f'A cancel charge of {charge} will be deducted from your booking fee'})
            except Exception:
                return "An error occurred while updating your task."
    

@app.route('/api/confirm-cancel-charge/', methods=['POST'])
@basic_auth.required
def comfirm_charge():
    data = request.get_json()
    id = decode_hashid(data['id'])[0]
    charge = data['charge']
    booking = Booking.query.get_or_404(id)
    booking.status = BookingStatusEnum.cancelled
    booking.cancel_charge = charge
    try:
        db.session.commit()
        return jsonify({'status': "ok" })
    except Exception:
        return jsonify({"error":"An error occurred while updating your task."})





######################## ADMIN VIEWS #################################################

# home
@app.route('/home')
def home():
    return render_template('index.html')


# Register User
#For admin
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            try:
                user = User(username=form.username.data, staff=form.staff.data, email=form.email.data)
                user.set_password(form.password1.data)
                print(user)
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            except Exception as e:
                flash(e.message)
        flash('User Already Registered')
    return render_template('registration.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('home'))
        flash('Invalid email address or Password.')
    return render_template('login.html', form=form)




@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/hotel-management', methods=['GET', 'POST'])
@login_required
def hotel_management():
    form = HotelForm()
    if form.validate_on_submit():
        hotel = Hotel(city=form.city.data, capacity=form.capacity.data,
                      peak_rate=form.peak_rate.data, off_peak_rate=form.off_peak_rate.data,
                      available=form.available.data, description=form.description.data
                      )
        try:
            db.session.add(hotel)
            db.session.commit()
            return redirect('/hotel-management')
        except Exception as e:
            flash(f"An error occured:\n {e}")
    hotels = Hotel.query.order_by(Hotel.date).all()
    return render_template('hotels.html', form=form, hotels=hotels)

@app.route('/hotel-management/update/<int:id>', methods=['GET', 'POST'])
@login_required
def hotel_update(id):
    # db.session.
    form = HotelForm()
    hotel = Hotel.query.get_or_404(id)
    if form.validate_on_submit():
        hotel.city=form.city.data 
        hotel.capacity=int(form.capacity.data)
        hotel.peak_rate=float(form.peak_rate.data)
        hotel.off_peak_rate=float(form.off_peak_rate.data)
        hotel.available=form.available.data 
        hotel.description=form.description.data
        try:
            db.session.commit()
            return redirect('/hotel-management')
        except Exception as e:
            flash(f"An error occured:\n {e}")
    return render_template('update_hotels.html', form=form, hotel=hotel)

@app.route('/hotel-management/delete/<int:id>', methods=['GET'])
@login_required
def hotel_delete(id):
    hotel = Hotel.query.get_or_404(id=id)
    try:
        db.session.delete(hotel)
        return redirect('/hotel-management')
    except Exception as e:
        flash(f"An error occured:\n {e}")



# @app.route('/book/<int:id>')
# def book(id):
#     hotel = Hotel.query.get_or_404(id)
#     details = get_room_details(hotel)
#     season = get_peak_season()
#     return render_template('book_hotel.html', details=details, id=id, season=season)


@app.route('/all-bookings/')
@login_required
def all_book():
    bookings = Booking.query.all()
    return render_template('all_bookings.html',bookings=bookings)

@app.route('/all-users/')
@login_required
def all_user():
    users = User.query.all()
    return render_template('all_users.html', users=users)


@app.route('/delete-user/<int:id>/')
@login_required
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
    except Exception:
        return "An error occurred while deleting task"
    return redirect(url_for('all_users'))

@app.route('/delete-booking/<int:id>/')
@login_required
def delete_book(id):
    book_to_delete = Booking.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
    except Exception:
        return "An error occurred while deleting task"
    return redirect(url_for('all_book'))


# @app.route('/confirm-booking/<int:id>/<type>/<season>/', methods=['GET', 'POST'])
# def confirm_booking(id, type, season):
#     hotel = Hotel.query.get_or_404(id)
#     prices = get_prices(hotel)
#     room_type = RoomTypeEnum.standard
#     user_id = current_user.id
#     amount_payable = 0
#     if type == 'standard':
#         amount_payable = prices['s_peak'] if season == 'peak' else prices['s_off_peak']
#     elif type == 'double':
#         room_type = RoomTypeEnum.double
#         amount_payable = prices['d_peak'] if season == 'peak' else prices['d_off_peak']
#     else:
#         room_type = RoomTypeEnum.family
#         amount_payable = prices['f_peak'] if season == 'peak' else prices['f_off_peak']
    
#     if request.method == 'POST':
#         print("Here")
#         date = request.form['date']
#         date = datetime.fromisoformat(date)
#         number_people = int(request.form['number_people'])
#         if room_type == RoomTypeEnum.double and number_people == 2:
#             amount_payable += amount_payable * 0.1
#         booking = Booking(user_id=user_id, hotel_id=id, status=BookingStatusEnum.not_paid,
#         room_type=room_type, date=date, number_people=number_people, amount=amount_payable)
#         try:
#             db.session.add(booking)
#             db.session.commit()
#             return redirect(url_for('makepayment', id=booking.id, amount_payable=amount_payable))
#         except Exception as e:
#             print(e)
#             return "An error occured while booking your room."
#     return render_template('confirm_booking.html', amount_payable=amount_payable, room_type=room_type)


# @app.route('/makepayment/<int:id>/<int:amount_payable>/',  methods=['GET', 'POST'])
# def makepayment(id, amount_payable):
#     booking = Booking.query.get_or_404(id)
#     discount_details = get_discount_rate(booking, amount_payable)
#     amount_payable = discount_details['to_pay']
#     if request.method == 'POST':
#         amount_payable = discount_details['to_pay']
#         booking.status = BookingStatusEnum.paid
#         booking.amount = amount_payable
#         try:
#             db.session.commit()
#             return redirect(url_for('my_bookings'))
#         except Exception as e:
#             print(e)
#             return f"{e}"
#     return render_template('pay.html', amount_payable=amount_payable, discount_details=discount_details)


@app.route('/my-bookings')
def my_bookings():
    bookings = Booking.query.order_by(Booking.id).all()
    return render_template('my_bookings.html', bookings=bookings)


@app.route('/cancel-bookings/<int:id>/', methods=['POST', 'GET'])
@login_required
def cancel_booking(id):
    user_id = current_user.id
    booking = Booking.query.get_or_404(id)
    charge = get_cancel_charge(booking)
    print(charge)
    if charge == 0:
        booking.status = BookingStatusEnum.cancelled
        try:
            db.session.commit()
            return redirect(url_for('my_bookings'))
        except Exception:
            return "An error occurred while updating your task."
    else:
        if request.method == 'POST':
            booking.status = BookingStatusEnum.cancelled
            booking.cancel_charge = charge
            try:
                db.session.commit()
                return redirect(url_for('my_bookings'))
            except Exception:
                return "An error occurred while updating your task."
        else:
            return render_template('pay_charge.html')



if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
