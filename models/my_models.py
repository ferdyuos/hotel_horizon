import enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class BookingStatusEnum(enum.Enum):
    paid = 'Paid'
    cancelled = 'Cancelled'
    not_paid = 'Not Paid'

class RoomTypeEnum(enum.Enum):
    standard = 'standard'
    double = 'double'
    family = 'family'

class SeasonTypeEnum(enum.Enum):
    peak = 'peak'
    off_peak = 'off-peak'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password_hash = db.Column(db.String(150))
    staff = db.Column(db.Boolean, default=False, nullable=False)
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    peak_rate = db.Column(db.Float(), nullable=False)
    off_peak_rate = db.Column(db.Float(), nullable=False)
    available = db.Column(db.Boolean(), default=False, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    booking = db.relationship('Booking', backref='hotel', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    hotel_id = db.Column(db.Integer(), db.ForeignKey('hotel.id'), nullable=False)
    room_type = db.Column(db.Enum(RoomTypeEnum), default=RoomTypeEnum.standard, nullable=False)
    status = db.Column(db.Enum(BookingStatusEnum), default=BookingStatusEnum.paid, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    number_people = db.Column(db.Integer(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    ref_code = db.Column(db.String(500), nullable=False)
    booked_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    season = db.Column(db.Enum(SeasonTypeEnum), default=SeasonTypeEnum.peak, nullable=False)
    cancel_charge = db.Column(db.Float(), default=0.0)

# class Booking(db.Model):