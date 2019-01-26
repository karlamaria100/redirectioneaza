
import webapp2
from os import environ

from appengine_config import SESSION_SECRET_KEY, DEV

from webapp2_extras import routes
from webapp2 import Route as r

from controllers.site import *
from controllers.account_management import *
from controllers.my_account import *
from controllers.api import *
from controllers.admin import *
from controllers.ngo import NgoHandler, TwoPercentHandler, DonationSucces

from cron import cron_routes

######################
# Update to Flask
######################
from flask import Flask 
from flask_script import Manager 

######################


config = {
    'webapp2_extras.auth': {
        'user_model': 'models.user.User',
        'user_attributes': ['first_name']
    },
    # by default the session backend is the cookie
    # cookie_name: session
    # session_max_age: None => until the client is closed
    'webapp2_extras.sessions': {
        'secret_key': SESSION_SECRET_KEY,
        # just make it as the default
        'cookie_name': 'session',
        'cookie_args': {
            # make the cookie secure only if we are on production
            # we can't use the config DEV bool, because if we set that manually to False, in order 
            # to test prod locally, the cookie will not work
            # so make sure the cookie are set to secure only in production
            'secure': not environ.get('SERVER_SOFTWARE', 'Development').startswith('Development'),
            'httponly': True
        }
    }
}

# # use string in dotted notation to be lazily imported
# app = webapp2.WSGIApplication([
#         # the public part of the app
#         r('/',                  handler=HomePage),
#         r('/ong',               handler=ForNgoHandler),
        
#         # backup in case of old urls. to be removed
#         r('/pentru-ong-uri',    handler=ForNgoHandler),
        
#         r('/asociatii',         handler=NgoListHandler),

#         r('/termeni',           handler=TermsHandler),
#         r('/TERMENI',           handler=TermsHandler),
#         r('/nota-de-informare', handler=NoteHandler,    name='note'),
#         r('/politica',          handler=PolicyHandler),
#         r('/despre',            handler=AboutHandler),

#         # account management
#         r('/cont-nou',  handler=SignupHandler),
#         r('/login',     handler=LoginHandler, name='login'),
#         r('/logout',    handler=LogoutHandler, name='logout'),

#         r('/forgot',    handler=ForgotPasswordHandler, name='forgot'),
        
#         # verification url: used for signup, and reset password
#         r('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', handler=VerificationHandler, name='verification'),
#         r('/password',  handler=SetPasswordHandler),
        
#         # my account
#         r('/contul-meu',        handler=MyAccountHandler, name='contul-meu'),
#         r('/asociatia',         handler=NgoDetailsHandler, name='asociatia'),
#         r('/date-cont',         handler=MyAccountDetailsHandler, name='date-contul-meu'),

#         r('/api/ngo/check-url/<ngo_url>',   handler=CheckNgoUrl,    name='api-ngo-check-url'),
#         r('/api/ngo/upload-url',            handler=GetUploadUrl,   name='api-ngo-upload-url'),
#         r('/api/ngo/form/<ngo_url>',        handler=GetNgoForm,     name='api-ngo-form-url'),
#         r('/api/ngos',                      handler=NgosApi,        name='api-ngos'),

#         # ADMIN HANDLERS
#         r('/admin',             handler=AdminHandler,       name='admin'),
#         r('/admin/conturi',     handler=UserAccounts,       name='admin-users'),
#         r('/admin/campanii',    handler=SendCampaign,       name='admin-campanii'),
#         r('/admin/ong-nou',     handler=AdminNewNgoHandler, name='admin-ong-nou'),
#         r('/admin/<ngo_url>',   handler=AdminNgoHandler,    name='admin-ong'),


#         r('/<ngo_url>',         handler=NgoHandler, name="ngo-url"),
#         r('/catre/<ngo_url>',   handler=NgoHandler),

#         r('/<ngo_url>/doilasuta',           handler=TwoPercentHandler,  name="twopercent"),
#         r('/<ngo_url>/doilasuta/succes',    handler=DonationSucces,     name="ngo-twopercent-success"),
#         r('/<ngo_url>/doilasuta/succes',    handler=DonationSucces,     name="ngo-twopercent-success"),

#         routes.PathPrefixRoute("/cron", cron_routes),
#     ],
#     debug=True,
#     config=config
# )

# error handling for 404 and 500
# imported from controllers.site
# app.error_handlers[404] = NotFoundPage
# app.error_handlers[500] = InternalErrorPage




######################
# Update to Flask
####################
app = Flask(__name__, template_folder="views")
app.secret_key = "secret"
app.config['DEBUG'] = True

manager = Manager(app)


# Routes
# TODO: check parameter types and test route if the same as the previous version

app.add_url_rule('/', 'home', view_func=HomePage.as_view('home'))
app.add_url_rule('/ong', 'ong', view_func=ForNgoHandler.as_view('ong'))

# backup in case of old urls. to be removed
app.add_url_rule('/pentru-ong-uri', 'pentru-ong-uri', view_func=ForNgoHandler.as_view('pentru-ong-uri'))
app.add_url_rule('/asociatii', 'asociatii', view_func=NgoListHandler.as_view('asociatii'))
# TODO: check daca merge si cu uppercase
app.add_url_rule('/termeni', 'termeni', view_func=TermsHandler.as_view('termeni'))
#         r('/TERMENI',           handler=TermsHandler),
app.add_url_rule('/nota-de-informare', 'note', view_func=NoteHandler.as_view('note'))
app.add_url_rule('/politica', 'politica', view_func=PolicyHandler.as_view('politica'))
app.add_url_rule('/despre', 'despre', view_func=AboutHandler.as_view('despre'))
#         # account management

app.add_url_rule('/cont-nou', 'cont-nou', view_func=SignupHandler.as_view('cont-nou'))
app.add_url_rule('/login', 'login', view_func=LoginHandler.as_view('cont-nou'), methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', view_func=LogoutHandler.as_view('cont-nou'))
app.add_url_rule('/forgot', 'forgot', view_func=ForgotPasswordHandler.as_view('forgot'))

#         # verification url: used for signup, and reset password
# TODO: check parameter types and test route if the same as the previous version
app.add_url_rule('/<string:type>/<int:user_id>-<string:signup_token>', 'verification', view_func=VerificationHandler.as_view('verification'))
#         r('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', handler=VerificationHandler, name='verification'),

app.add_url_rule('/password', 'password', view_func=SetPasswordHandler.as_view('password'))

#         # my account
app.add_url_rule('/contul-meu', 'contul-meu', view_func=MyAccountHandler.as_view('contul-meu'))
app.add_url_rule('/asociatia', 'asociatia', view_func=NgoDetailsHandler.as_view('asociatia'), methods=['GET', 'POST'])
app.add_url_rule('/date-cont', 'date-cont', view_func=MyAccountDetailsHandler.as_view('date-contul-meu'), methods=['GET', 'POST'])
app.add_url_rule('/api/ngo/check-url/<ngo_url>', 'api-ngo-check-url', view_func=CheckNgoUrl.as_view('api-ngo-check-url'))
app.add_url_rule('/api/ngo/upload-url', 'api-ngo-upload-url', view_func=GetUploadUrl.as_view('api-ngo-upload-url'))
app.add_url_rule('/api/ngo/form/<ngo_url>', 'api-ngo-form-url', view_func=GetNgoForm.as_view('api-ngo-form-url'))
app.add_url_rule('/api/ngos', 'api-ngos', view_func=NgosApi.as_view('api-ngos'))

#         # ADMIN HANDLERS
app.add_url_rule('/admin', 'admin', view_func=AdminHandler.as_view('admin'))
app.add_url_rule('/admin/conturi', 'admin-users', view_func=UserAccounts.as_view('admin-users'))
app.add_url_rule('/admin/campanii', 'admin-campanii', view_func=SendCampaign.as_view('admin-campanii'))
app.add_url_rule('/admin/ong-nou', 'admin-ong-nou', view_func=AdminNewNgoHandler.as_view('admin-ong-nou'))
app.add_url_rule('/admin/<ngo_url>', 'admin-ong', view_func=AdminNgoHandler.as_view('admin-ong'))

app.add_url_rule('/<ngo_url>', 'ngo-url', view_func=NgoHandler.as_view('ngo-url'))
app.add_url_rule('/catre/<ngo_url>', 'catre-ngo-url', view_func=NgoHandler.as_view('catre-ngo-url'))
app.add_url_rule('/<ngo_url>/doilasuta', 'twopercent', view_func=NgoHandler.as_view('twopercent'))
app.add_url_rule('/<ngo_url>/doilasuta/succes', 'doilasuta-succes', view_func=DonationSucces.as_view('ngo-twopercent-success'))
