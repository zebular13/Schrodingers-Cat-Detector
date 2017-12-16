"""
Runs that functionality of the program, the flask app and the server that communicates with Walabot.
"""

from threading import Thread

from howIsCat import app

def main():
    """
    Start the server that communicates with Walabot and the flask app that communicates with Alexa.
    """
    try:
        alexa_server_thread = Thread(target=app.run)

        alexa_server_thread.start()

        alexa_server_thread.join()

    except Exception:
        print("Unknown exception occurred!")
        raise

if __name__ == '__main__':
    main()