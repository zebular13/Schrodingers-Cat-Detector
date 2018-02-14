"""
Initialize and configure the Walabot. Check on the cat and start sending data to the server.
"""
from __future__ import print_function # wlbt works on both Python 2 and 3.
from flask import Flask
from flask_ask import Ask, statement
from datetime import datetime  # used to the current time
from sys import platform
from imp import load_source

app = Flask(__name__)
ask = Ask(app, '/')

wlbt = load_source('WalabotAPI',
    'C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI.py')
#from api.walabot_api import WalabotAPI

R_MIN, R_MAX, R_RES = 30, 100, 2  # SetArenaR parameters
THETA_MIN, THETA_MAX, THETA_RES = 0, 10, 10  # SetArenaTheta parameters
PHI_MIN, PHI_MAX, PHI_RES = 0, 10, 2  # SetArenaPhi parametes
#THRESHOLD = 15  # SetThreshold parameters
ASSUMED_FRAME_RATE = 10
# TODO: Need to be configured to real server's ip and port
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 9999

#from imp import load_source
#wlbt = load_source(‘WalabotAPI’,
#‘C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI.py’)

wlbt.Init()
# Configure Walabot database install location (for windows)
wlbt.SetSettingsFolder()

catStatus = 2 #declare global variable schrodinger's cat
breathLimit = 0.0005 # below 0.0005 is background for derivative mode
               # 0.01 for NONE filter mode works for about 50cm

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
    
def verifyWalabotIsConnected():
    """ Check for Walabot connectivity. loop until detect a Walabot.
    """
    while True:
        try:
            wlbt.ConnectAny()
        except wlbt.WalabotError as err:
            input("- Connect Walabot and press 'Enter'.")
        else:
            print('- Connection to Walabot established.')
            return

def setWalabotSettings():
    """ Configure Walabot's profile, arena (r, theta, phi), threshold and
        the image filter.
    """
    wlbt.SetProfile(wlbt.PROF_SENSOR)
    wlbt.SetArenaR(R_MIN, R_MAX, R_RES)
    wlbt.SetArenaTheta(THETA_MIN, THETA_MAX, THETA_RES)
    wlbt.SetArenaPhi(PHI_MIN, PHI_MAX, PHI_RES)
    #wlbt.SetThreshold(THRESHOLD)
    wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_DERIVATIVE) #Also test with FILTER_TYPE_NONE
    print('- Walabot Configured.')

def startAndCalibrateWalabot():
    """ Start the Walabot and calibrate it.
    """
    wlbt.StartCalibration()
    print('- Calibrating...')
    while wlbt.GetStatus()[0] == wlbt.STATUS_CALIBRATING:
        wlbt.Trigger()
    wlbt.Start()
    print('- Calibration ended.\n- Ready!')

def stopAndDisconnectWalabot():
    """ Stops Walabot and disconnects the device.
    """
    wlbt.Stop()
    wlbt.Disconnect()
    print ('Termination successful')

def catExists():
    """ Detect and record whether or not there is a target and whether or not it is breathing.
        Returns:
        dataList: A list of pairs of whether or not there was a target and whether or not it was moving
    """
    
    currentTime = datetime.now().strftime('%H:%M:%S')
    while True:
        wlbt.Trigger()
        target = wlbt.GetSensorTargets()
        if target:
            breathing = isBreathing()
            if breathing == 1:
                print("the cat is alive!")
                catStatus = 2
            else:
                print("the cat is dead!")
                catStatus = 1
        else:
            print("There's no cat in this box")
            catStatus = 0
        return catStatus

def isBreathing():
    breath = wlbt.GetImageEnergy()
    # use image energy of walabot to detect breathing
    if breath > breathLimit:
    # if the current average range of image energy is above the threshhold
    # the cat is breathing
        return 1
    else:
        return 0

def SchrodingersCat():
    """ Main function. init and configure the Walabot, get the cat status.
        Walabot scan constantly and record sets of data (when peoples are
        near the door header).
    """
    # 1) Connect: Establish communication with walabot.
    verifyWalabotIsConnected()
    # 2) Configure: Set scan profile and arena
    setWalabotSettings()
    # 3) Start: Start the system in preparation for scanning.
    startAndCalibrateWalabot()
    
    #whenever the socket is connected, get the cat's status
    while True:
        catStatus = catExists()
        print(catStatus)
   
    #7) Stop and Disconnect.
    #except KeyboardInterrupt:
    #    pass
    #finally:
    #    stopAndDisconnectWalabot()

    
if __name__ == '__main__':
    SchrodingersCat()