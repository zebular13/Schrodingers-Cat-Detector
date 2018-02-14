"""
Runs that functionality of the program, the flask app and the server that communicates with Walabot.
"""
#from os import system
import sys
from subprocess import Popen, PIPE
from threading import Thread
from howIsCat import app
from SchrodingersCat import SchrodingersCat

def main():
    """
    Start the flask app that communicates with Alexa.
    TO DO:
    Currently Alexa can't communicate with the app because the walabot data takes up the whole "thread"
    """
    try:
        #system('python schrodingerscat.py')
        process = Popen([sys.executable, 'schrodingerscat.py'])
        process.communicate()

        #start the alexa skill on a separate thread
        alexa_server_thread = Thread(target=app.run)

        alexa_server_thread.start()

        alexa_server_thread.join()

    except Exception:
        print("Unknown exception occurred!")
        raise

if __name__ == '__main__':
    main()