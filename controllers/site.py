# -*- coding: utf-8 -*-

from google.appengine.ext.ndb import get_multi

from appengine_config import DEFAULT_NGO_LOGO
from models.handlers import BaseHandler
from models.models import NgoEntity

from random import sample
from logging import info

import json
from flask import render_template, request, redirect, url_for, session

"""
Handlers used for site routing
"""
class HomePage(BaseHandler):
    template_name = 'index.html'

    # def dispatch_request(self):
    def get(self):

        self.template_values["title"] = "redirectioneaza 2%"

        try:
            list_keys = NgoEntity.query(NgoEntity.active == True).fetch(keys_only=True)
            list_keys = sample(list_keys, 4)
            
            ngos = get_multi(list_keys)
        except Exception, e:
            info(e)
            ngos = NgoEntity.query.filter(NgoEntity.active == True).fetch(4)

        self.template_values["ngos"] = ngos
        self.template_values["DEFAULT_NGO_LOGO"] = DEFAULT_NGO_LOGO
                
        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()


        ######################
        # Update to Flask - add method:
        ####################
        # render a response
        return self.render()

        # return render_template(self.template_name, **self.template_values)


class ForNgoHandler(BaseHandler):
    template_name = 'for-ngos.html'
    def get(self):
        # self.abort(404)
        self.template_values["title"] = "Pentru ONG-uri"

        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()


class NgoListHandler(BaseHandler):
    template_name = 'all-ngos.html'
    def get(self):
        # self.abort(404)
        self.template_values["title"] = "Asociatii"

        ngos = NgoEntity.query(NgoEntity.active == True).fetch()
        self.template_values["ngos"] = ngos
        self.template_values["DEFAULT_NGO_LOGO"] = DEFAULT_NGO_LOGO

        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()

class TermsHandler(BaseHandler):
    template_name = 'terms.html'
    def get(self):

        self.template_values["title"] = "Termeni si conditii"

        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()

class NoteHandler(BaseHandler):
    template_name = 'note.html'
    def get(self):

        self.template_values["title"] = "Nota de informare"

        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()

class AboutHandler(BaseHandler):
    template_name = 'despre.html'
    def get(self):

        self.template_values["title"] = "Despre Redirectioneaza.ro"

        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()

class PolicyHandler(BaseHandler):
    template_name = 'policy.html'
    def get(self):

        self.template_values["title"] = "Politica de confidentialitate"

        ######################
        # update to flask - add method:
        ####################
        # render a response
        return self.render()

def NotFoundPage(request, response, exception):
    """handles the 404 page
        we can't use BaseHandler for this page. 
        webapp2 only accepts a simple function like this one
    """
    
    # create a mock handler so we can user templates
    handler = BaseHandler(request, response)

    response.set_status(404)

    handler.render('404.html')

def InternalErrorPage(request, response, exception):
    """handles the 500 page. same as the 404 page
    """
    
    # create a mock handler so we can user templates
    handler = BaseHandler(request, response)

    from logging import critical

    critical(exception, exc_info=1)

    response.set_status(500)

    handler.render('500.html')
