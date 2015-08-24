

from google.appengine.ext import ndb

from appengine_config import LIST_OF_COUNTIES


class BaseEntity(ndb.Model):
    """basic type of model that all other inherit from
        mainly just a wrapper for ndb.Model
    """
    pass



# to the list of counties add the whole country
county_choices = LIST_OF_COUNTIES + ["RO", ""]
class NgoEntity(BaseEntity):

    name = ndb.StringProperty(indexed=True)
    short_description = ndb.StringProperty(indexed=True)

    description = ndb.TextProperty()

    logo = ndb.StringProperty(indexed=True)
    # the background image that will go above the description
    image = ndb.StringProperty(indexed=True)
    
    account = ndb.StringProperty(indexed=True)
    cif = ndb.StringProperty(indexed=True)
    address = ndb.TextProperty()
    county = ndb.StringProperty(indexed=True, choices=county_choices)

    # the ngo's phone number
    tel = ndb.StringProperty(indexed=True)
    # the main email address used as contact
    email = ndb.StringProperty(indexed=True)
    website = ndb.StringProperty(indexed=True)
    # a list of email addresses
    other_emails = ndb.StringProperty(indexed=True, repeated=True)

    # if the ngo verified its existance
    verified = ndb.BooleanProperty(indexed=True, default=False)
    # bool telling if the ngo should be shown to the public
    # the ngo might be banned
    active = ndb.BooleanProperty(indexed=True, default=True)

    document_urls = ndb.StringProperty(indexed=True, repeated=True)


    # tags for the 
    tags = ndb.StringProperty(indexed=True, repeated=True)

    # meta data
    date_created = ndb.DateTimeProperty(indexed=True, auto_now_add=True)

    # bool telling if the ngp wants to allow the donor to upload the signed document
    allow_upload = ndb.BooleanProperty(indexed=True, default=False)


class Fundraiser(BaseEntity):
    pass

class Donor(BaseEntity):
    
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    
    city = ndb.StringProperty(indexed=True)
    county = ndb.StringProperty(indexed=True)
    
    email = ndb.StringProperty(indexed=True)
    tel = ndb.StringProperty()

    geoip = ndb.TextProperty()

    ngo = ndb.KeyProperty(kind="NgoEntity")

    # the pdf to be downloaded by the donor
    pdf_url = ndb.StringProperty()
    # the url of the pdf/image after it was signed and scanned
    # only if the ngo allows it
    pdf_signed_url = ndb.StringProperty()

    # meta data
    date_created = ndb.DateTimeProperty(indexed=True, auto_now_add=True)


events = ["log-in", "form-submitted"]
class Event(BaseEntity):
    what = ndb.StringProperty(indexed=True, choices=events)

    who = ndb.KeyProperty()

    when = ndb.DateTimeProperty(indexed=True, auto_now_add=True)
