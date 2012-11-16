import webapp2
import model
from google.appengine.ext import ndb

import string

def make_rot_n(n):
    lc = string.lowercase
    uc = string.uppercase
    trans = string.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return lambda s: string.translate(s, trans)

def rotate(text, rot):
    rot = int(rot)
    text = text.encode('ascii', 'ignore').strip()
    return make_rot_n(rot)(text)

class DecryptHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("GET was called")

    def post(self):
        rot = self.request.get('rotate')
        text_key = self.request.get('text')
        text_key = "caesar"
        text = ndb.Key(model.Text, text_key).get()
        self.response.out.write(rotate(text.encrypted, rot))

