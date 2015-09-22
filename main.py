import os
import re
from google.appengine.ext import db
import webapp2
import jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        return render_str(template, **params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class Contact(db.Model):
    name = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    mobile_no = db.StringProperty(required = True)
    subject = db.TextProperty(required = True)
#Delete this block after deploying this source code once.     
#c = Contact(name = "Manas Chaturvedi", email = "manas.oid@gmail.com", 
#            mobile_no = 9022380436, subject = "I want my house renovated !")  

#c.put()
#End of block   

class ContactHandler(BlogHandler):    
    def get(self,p):
        self.render("contact.html")
    def post(self,p):
        name = self.request.get("name")
        email = self.request.get("email")
        mobile_no = self.request.get("mobile_no")
        subject = self.request.get("subject")
        if subject and name and mobile_no and email:
            d = Contact(name = name, email = email,mobile_no = mobile_no, subject = subject)
            d.put()
            error = "thank you submitting your query we will get to you shortly"
            self.render("contact.html", error=error)   
        else:
            error = "please!!! fill all the information"
            self.render("contact.html", error=error)    

class MainHandler(BlogHandler):
    def get (self, q):
        if q is None:
            q = 'index.html'
        self.response.headers ['Content-Type'] = 'text/html'
        self.render(q)
        
app = webapp2.WSGIApplication([('/contact(.*html)?', ContactHandler),('/(.*html)?', MainHandler)],debug=True)        