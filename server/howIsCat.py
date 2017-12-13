"""
Export The flask app that will communicate with alexa.
"""

from flask import Flask
from flask_ask import Ask, statement
from tinydb import Query

from DBHandler import DBHandler as TinyDB
from config import DB_PATH, CAT_STATUS_FIELD

app = Flask(__name__)
ask = Ask(app, '/')
db = TinyDB(DB_PATH)
CatInBox = Query()

@ask.intent('SchrodingersCatIntent')
def how_is_cat():
    """
    Check to see if the cat is alive or dead
    """
    cat_status = db.get(CatInBox.cat_status_field)
    if cat_status is None:
         return statement("I'm sorry, I am not getting information from the box. Please check if Walabot"
                          "is working correctly.")
    if cat_status == 1:
        return statement("Schrodinger's cat is dead")
    if cat_status == 2:
        return statement("Schrodingers cat is alive")
    if cat_status == 0:
        return statement("There's no cat in the box! It looks like Schodinger's cat has escaped.")
    return statement("Schrodingers cat is great today.")