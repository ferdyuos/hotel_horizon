import random  # define the random module
import string
import re
from flask import current_app, Response, jsonify, render_template
import flask
from hashids import Hashids
from constants import BASE_DIR
from models.my_models import Booking, BookingStatusEnum, RoomTypeEnum
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO, StringIO
import jinja2
from models.my_models import db
import json
from flask import make_response, send_file 
from pathlib import Path
import pdfkit
_SECRET_KEY = '56c18f6f1e221f65dead591a8c6802942ab8d03a721e5986'



def create_hashid(id):
    hashids = Hashids(min_length=5, salt="hjdabckd-121kf hsaca-dkjsbvds")
    hashid = hashids.encode(id)
    return hashid


def decode_hashid(hashid):
    hashids = Hashids(min_length=5, salt="hjdabckd-121kf hsaca-dkjsbvds")
    id = hashids.decode(hashid)
    return id


def get_prices(hotel):
        #peak season rates
    s_peak = hotel.peak_rate
    d_peak = s_peak + round((s_peak * 0.2), 2)
    f_peak = s_peak + round((s_peak * 0.5), 2)

    # off peak season rate
    s_off_peak = hotel.off_peak_rate
    d_off_peak = s_off_peak + round((s_off_peak * 0.2), 2)
    f_off_peak = s_off_peak + round((s_off_peak * 0.5), 2)

    return {'s_peak':s_peak, 
    's_off_peak':s_off_peak,
    'd_peak':d_peak, 
    'd_off_peak':d_off_peak, 
    'f_peak':f_peak, 
    'f_off_peak':f_off_peak,}

def get_room_capacity(hotel):
    capacity = hotel.capacity
    # total number of room type
    s_room_total = int(capacity * 0.3)
    d_room_total = int(capacity * 0.5)
    f_room_total = int(capacity * 0.2)

    # TO get the number of rooms that are available
    bookings = Booking.query.filter(Booking.hotel_id == hotel.id).filter(Booking.status == BookingStatusEnum.paid).all()
    s_count, d_count, f_count = 0, 0, 0
    if bookings:
        for book in bookings:
            if book.room_type == RoomTypeEnum.standard:
                s_count += 1
            elif book.room_type == RoomTypeEnum.double:
                d_count += 1
            else:
                f_count += 1
        s_room_total -= s_count
        d_room_total -= d_count
        f_room_total -= f_count
            
    return {'s_room_total':s_room_total, 'd_room_total':d_room_total, 'f_room_total':f_room_total} 
def get_room_details(hotel):
    """Takes a room as a parameter and returns a tuple of it's details
    
    Keyword arguments:
    argument -- hotel an instance of the hotel model
    Return: a tuple of room details 
    """

    # number of guests
    s_guest = 1
    d_guest = 2
    f_guest = 6

    price = get_prices(hotel)
    capacity = get_room_capacity(hotel)

    return [
        {"type":"standard", 'guest':s_guest, 'peak':price['s_peak'], 'off_peak':price['s_off_peak'], 'room_total':capacity['s_room_total']},
        {"type":"double",'guest':d_guest, 'peak':price['d_peak'], 'off_peak':price['d_off_peak'], 'room_total':capacity['d_room_total']},
        {"type":"family",'guest':f_guest, 'peak':price['f_peak'], 'off_peak':price['f_off_peak'], 'room_total':capacity['f_room_total']}
    ]

    
def get_peak_season():
    seasons = [4,5,6,7,8,9]
    month = datetime.now().month

    if month in seasons:
        return 'peak'
    else:
        return 'off-peak'

def get_cancel_charge(booking):
    date = booking.date
    now = datetime.utcnow()
    days = (date - now).days
    charges = 0
    if booking.status == BookingStatusEnum.paid:
        if days >= 60:
            pass
        elif days >= 31 and days <= 59:
            charges = booking.amount * 0.5
        elif days >= 0 and days <= 30:
            charges = booking.amount
        return charges



def get_discount_rate(booking, amount_payble):
    date = booking.date
    now = datetime.utcnow()

    days = (date.replace(tzinfo=None) - now.replace(tzinfo=None) ).days
    if days >= 80 and days <= 90:
        to_pay = amount_payble - (amount_payble * 0.2)
        return {'message': 'You have been given a 20% \discount', 'to_pay':to_pay}
    elif days >= 60 and days <= 79:
        to_pay = amount_payble - (amount_payble * 0.1)
        return {'message': 'You have been given a 10% \discount', 'to_pay':to_pay}
    elif days >=45 and days <= 59:
        to_pay = amount_payble - (amount_payble * 0.05)
        return {'message': 'You have been given a 5% \discount', 'to_pay':to_pay}
    else:
        return {'message':'No discount availabe','to_pay':amount_payble}


def render_to_pdf(context_dict={}):
    TEMPLATE_FILE = "ticket.html"
    html = flask.render_template( TEMPLATE_FILE,booking=context_dict['booking'], user=context_dict['user'])
    result_file = open(f'{BASE_DIR}/documents/ticket.pdf', "w+b")
    pisa_status = pisa.CreatePDF(
            src=html,
            dest=result_file
        )   
    result_file.close()
    if pisa_status.err:
        return {'err': 'Error occured'}
    return {'path': f"{BASE_DIR}/documents/ticket.pdf"}


def get_ref_code(num: int):
    """ num is an int value. that decides how many caracters would be generated"""
    # call random.choices() string module to find the string in Uppercase + numeric data.
    _ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
    return _ran
