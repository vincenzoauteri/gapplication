import os 
from google.appengine.ext import db
import webapp2
import re
import cgi
from security import *
import jinja2
import logging
from mail import *

jinja_env = jinja2.Environment(
        autoescape=True, loader = jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))


#General 
def render_str(template, **params):
    """Function that render a jinja template with string substitution"""
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    """General class to render http response"""

    def write(self, *a, **kw):
        """Write generic http response with the passed parameters"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Utility function that can add new stuff to parameters passed"""
        params['style']='cerulean'
        if self.user : 
          params['welcome']='%s' % self.user.username
          params['logout']='Logout'
        else :
          params['welcome']='Login'
          params['login']='Login'
          params['signup']='Signup'

        return render_str(template, **params)

    def render(self, template, **kw):         
        """Render jinja template with named parameters"""
        self.write(self.render_str(template, **kw))
    
    def set_secure_cookie(self, name, val):
        """Send a http header with a hashed cookie"""
        hashed_cookie = make_cookie_hash(val)
        self.response.headers.add_header('Set-Cookie',
              "%s=%s; Path='/'" % (name,hashed_cookie))

    def read_secure_cookie(self, name):
        """Check if requesting browser sent us a cookie"""
        hashed_cookie = self.request.cookies.get(name)
        logging.error("Cookie name %s hash %s" % (name,hashed_cookie)) 
        if hashed_cookie :
            return verify_cookie_hash(hashed_cookie)
        else:
            return None

    def initialize(self, *a, **kw):
        """Function called before requests are processed.
           Used to check for sent cookies"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.get_by_id(int(uid))




class GentEnHandler(Handler):
    """Js impress handler"""

    def render_front(self, entries={}):
        self.render('gent-english.html')

    def get(self):
        self.render_front()

class GentEsHandler(Handler):
    """Js impress handler"""

    def render_front(self, entries={}):
        self.render('gent-spanish.html')

    def get(self):
        self.render_front()

class MapssHandler(Handler):
    """Maps handler"""

    def render_front(self, entries={}):
        self.render('maps.html',entries={"api-key":"10","sensor":"TRUE"})
    # entries={"api-key":"10","sensor":"TRUE"}

    def get(self):
        self.render_front()

class MapsHandler(webapp2.RequestHandler):
  def get(self):
    template_values =  {
        "apikey":"AIzaSyDGtBNgslf1vo9524bkFwArnIqaTffNX-Y",
        "sensor":"true"
        }

    template = jinja_env.get_template('maps.html')
    self.response.out.write(template.render(template_values))


class FrontPageHandler(Handler):
    """Class used to render the main page of the site"""

    def render_front(self, entries={}):
        """utility function used to render the front page"""
        self.render('index.html')

    def get(self):
        """Function called when the front page is requested"""
        self.render_front()


