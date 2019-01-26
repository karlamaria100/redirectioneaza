from flask_sqlalchemy import SQLAlchemy
import datetime
from appengine_config import DEFAULT_NGO_LOGO

db = SQLAlchemy()


# class BaseEntity(db.Model):
#     """basic type of model that all other inherit from
#         mainly just a wrapper for db.Model
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     pass



# to the list of counties add the whole country
class NgoEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    description = db.Column(db.Text)

    logo = db.Column(db.String(255), default=DEFAULT_NGO_LOGO)
    # the background image that will go above the description, if any
    image = db.Column(db.String(255))

    # the bank account
    account = db.Column(db.String(255))
    cif = db.Column(db.String(255))
    address = db.Column(db.Text)
    county = db.Column(db.String(255))

    # the ngo's phone number
    tel = db.Column(db.String(255))
    # the main email address used as contact
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    # a list of email addresses
    other_emails = db.Column(db.ARRAY(db.String(255)))

    # if the ngo verified its existence
    verified = db.Column(db.Boolean, default=False)

    # if the ngo has a special status (eg. social ngo) they are entitled to 3.5% donation, not 2%
    special_status = db.Column(db.Boolean, default=False)

    # bool telling if the ngo should be shown to the public (the ngo might be banned)
    active = db.Column(db.Boolean, default=True)

    # url to the ngo's 2% form, that contains only the ngo's details
    form_url = db.Column(db.String(255))

    # tags for the
    tags = db.Column(db.ARRAY(db.String(255)))

    # meta data
    date_created = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    # bool telling if the ngp wants to allow the donor to upload the signed document
    allow_upload = db.Column(db.Boolean(), default=False)


class Fundraiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pass

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    city = db.Column(db.String(255))
    county = db.Column(db.String(255))

    email = db.Column(db.String(255))
    tel = db.Column(db.String(255))

    anonymous = db.Column(db.Boolean(255), default=True)

    geoip = db.Column(db.Text)

    ngo = db.Column(db.ForeignKey("NgoEntity"))

    # the pdf to be downloaded by the donor
    pdf_url = db.Column(db.String(255))
    # the url of the pdf/image after it was signed and scanned
    # only if the ngo allows it
    pdf_signed_url = db.Column(db.String(255))

    # meta data
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


events = ["log-in", "form-submitted"]
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what = db.Column(db.Enum("log-in", "form-submitted"))

    who = db.Column(db.ForeignKey("Donor"))

    when = db.Column(db.DateTime, default=datetime.datetime.utcnow)
