"""
Export The flask app that will communicate with alexa.
"""

from flask import Flask
from flask_ask import Ask, statement
from tinydb import Query

from DBHandler import DBHandler as TinyDB
from config import CAT_DATA_TABLE, DB_PATH, CAT_STATUS_FIELD

app = Flask(__name__)
ask = Ask(app, '/')
db = TinyDB(DB_PATH, default_table=CAT_DATA_TABLE)
cat_in_box = Query()

@ask.intent('SchrodingersCatIntent')
def how_is_cat():
    """
    Check to see if the cat is alive or dead
    """
    if db.search(cat_in_box.cat_status_field.exists()):
        cat_status = db.get(doc_id=1)
        
        print(cat_status[CAT_STATUS_FIELD])
        if cat_status[CAT_STATUS_FIELD] == 1:
            return statement("Schrodinger's cat is dead")
        if cat_status[CAT_STATUS_FIELD] == 2:
            return statement("Schrodinger's cat is alive")
        if cat_status[CAT_STATUS_FIELD] == 0:
            return statement("There's no cat in the box! It looks like Schodinger's cat has escaped.")
        else:
            return statement("Schrodinger's cat is great today.")
    else:
        return statement("I'm sorry, I am not getting information from the box. Please check if Walabot"
                              "is working correctly.")