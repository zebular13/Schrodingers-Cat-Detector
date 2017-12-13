"""
Export The flask app that will communicates with alexa.
"""


from flask import Flask
from flask_ask import Ask, statement
from tinydb import Query

from DBHandler import DBHandler as TinyDB
from config import CAT_DATA_TABLE, DB_PATH, CAT_STATUS_FIELD

app = Flask(__name__)
ask = Ask(app, '/')
db = TinyDB(DB_PATH, default_table=CAT_DATA_TABLE)
cat_status_field = Query()

@ask.intent('SchrodingersCatIntent')
def how_is_cat(cat_status_field):
    """
    Check to see if the cat is alive or dead
    """
    # if cat_status_field is None:
    #     return statement("I'm sorry, I am not getting information from the box. Please check if Wala-bot"
    #                      "is working correctly.".format(cat_status_field))
    if cat_status_field == 1:
        return statement("Schrodinger's cat is dead".format(cat_status_field))
    if cat_status_field == 2:
        return statement("Schrodingers cat is alive".format(cat_status_field))
    if cat_status_field == 0:
        return statement("There's no cat in the box! It looks like Schodinger's cat has escaped.")
    #return statement("Schrodingers cat is great today.".format(cat_status_field))