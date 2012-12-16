import webapp2
import os
import jinja2

import model
import decrypt

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


results = {}

default_levels = []

level_list = None

defaultLevels = ['caesar']

def getOrCreateLevel(level_key):
    level = level_key.get()
    if not level:
        level = model.Level(key=level_key)
    return level


def resetText(text_id, name):
    key = ndb.Key(model.Text, text_id)
    text = key.get()
    if not text:
        text = model.Text(key=key)
    text.name = name
    text.content = open('texts/%s.txt' % text_id, 'rU').read()
    text.encrypted = decrypt.getEncrypter(text_id)(text.content)
    text.put()


def resetLevel(level_id, name, text_id):
    l1key = ndb.Key(model.Level, level_id)
    if not l1key in level_list.levels:
        level_list.levels.append(l1key)
        level_list.put()

    level = getOrCreateLevel(l1key)
    level.name = name
    level.startstory = open('texts/%s_start.txt' % level_id, 'rU').read()
    level.endstory = open('texts/%s_end.txt' % level_id, 'rU').read()
    level.text = ndb.Key(model.Text, text_id)
    key = level.put()
    results[level_id] = level
    return level
    

def resetAllTheThings():
    global default_levels
    global level_list

    level_list_key = ndb.Key(model.LevelSequence, model.LEVEL_LIST)
    level_list = level_list_key.get()
    if not level_list:
        # Create level list with level 1
        level_list = model.LevelSequence(key=level_list_key)
        level_list.name = 'default'
        level_list.put()

    # Filler text
    resetText('janeeyre', 'Jane Eyre')

    # Level 1 - Caesar Cipher
    resetText('caesar', 'Caesar Cipher Wikipedia Page')
    resetLevel('caesar', 'Julius Caesar', 'caesar')

    # Level 2 - ROT 13
    resetLevel('railenvy', 'Rail Envy', 'janeeyre')

    # Level 3 - Last Rotation Cipher
    resetLevel('oneshot', 'You got one shot at this', 'janeeyre')

    # Level 4 - Translation Cipher 1: UPINASI



class ResetHandler(webapp2.RequestHandler):
    def get(self):
        resetAllTheThings()

        values = {'results':results, 'levels':default_levels, 'level_list':level_list}

        template = jinja_environment.get_template('reset.html')
        self.response.out.write(template.render(values))

app = webapp2.WSGIApplication([
    ('/resetdata', ResetHandler),
], debug=True)
