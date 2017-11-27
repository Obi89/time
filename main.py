#!/usr/bin/env python
import os
import jinja2
import webapp2
from datetime import datetime
import pytz


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        utc = pytz.utc
        vienna = pytz.timezone('Europe/Vienna')
        utc_dt = utc.localize(datetime.now())
        vie_dt = utc_dt.astimezone(vienna)
        time = vie_dt.strftime('%Y-%m-%d %H:%M:%S %Z')
        return self.render_template("time.html", params={"time": time})


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
