"""
Export The flask app that will communicate with alexa.
"""
from flask import Flask
from flask_ask import Ask, statement
from SchrodingersCat import catStatus

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('SchrodingersCatIntent')
def how_is_cat():
    """
    Check to see if the cat is alive or dead
    """
    if catStatus is None:
        return statement("I'm sorry, I am not getting information from the box. Please check if Walabot"
                          "is working correctly.")
        print(catStatus)
    if catStatus == 1:
        return statement("Schrodinger's cat is dead")
        print(cat_status)
    if catStatus == 2:
        return statement("Schrodingers cat is alive")
        print(catStatus)
    if catStatus == 0:
        return statement("There's no cat in the box! It looks like Schodinger's cat has escaped.")
        print(catStatus)
    return statement("Schrodingers cat is great today.")

if __name__ == '__main__':
    HowIsCat()