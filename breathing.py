from __future__ import print_function # WalabotAPI works on both Python 2 and 3.
from sys import platform
from os import system
from imp import load_source
WalabotAPI = load_source('WalabotAPI',
    'C:/Program Files/Walabot/WalabotSDK/python/WalabotAPI.py')
WalabotAPI.Init()
def PrintSensorTargets(targets):
    system('cls' if platform == 'win32' else 'clear')
    if targets:
        for i, target in enumerate(targets):
            print (('Target #{}:\ntype: {}\nangleDeg: {}\nx: {}\ny: {}\nz: {}'+
                '\nwidth: {}\namplitude: {}\n').format(i + 1, target.type,
                target.angleDeg, target.xPosCm, target.yPosCm, target.zPosCm,
                target.widthCm, target.amplitude))
    else:
        print ('No Target Detected')
def InWallApp():
    # WalabotAPI.SetArenaX - input parameters
    xArenaMin, xArenaMax, xArenaRes = -3, 4, 0.5
    # WalabotAPI.SetArenaY - input parameters
    yArenaMin, yArenaMax, yArenaRes = -6, 4, 0.5
    # WalabotAPI.SetArenaZ - input parameters
    zArenaMin, zArenaMax, zArenaRes = 3, 8, 0.5
    # Configure Walabot database install location (for windows)
    WalabotAPI.SetSettingsFolder()
    # 1) Connect: Establish communication with walabot.
    WalabotAPI.ConnectAny()
    # 2) Configure: Set scan profile and arena
    # Set Profile - to Short-range.
    WalabotAPI.SetProfile(WalabotAPI.PROF_SHORT_RANGE_IMAGING)
    # Set arena by Cartesian coordinates, with arena resolution
    WalabotAPI.SetArenaX(xArenaMin, xArenaMax, xArenaRes)
    WalabotAPI.SetArenaY(yArenaMin, yArenaMax, yArenaRes)
    WalabotAPI.SetArenaZ(zArenaMin, zArenaMax, zArenaRes)
    # Walabot filtering disable
    WalabotAPI.SetDynamicImageFilter(WalabotAPI.FILTER_TYPE_NONE)
    # 3) Start: Start the system in preparation for scanning.
    WalabotAPI.Start()
    # calibrates scanning to ignore or reduce the signals
    WalabotAPI.StartCalibration()
    while True:
        appStatus, calibrationProcess = WalabotAPI.GetStatus()
        # 5) Trigger: Scan (sense) according to profile and record signals
        # to be available for processing and retrieval.
        WalabotAPI.Trigger()
        # 6) Get action: retrieve the last completed triggered recording
        targets = WalabotAPI.GetImagingTargets()
        rasterImage, sliceDepth, power = WalabotAPI.GetRawImageSlice()
        # print targets found
        PrintSensorTargets(targets)
    # 7) Stop and Disconnect.
    WalabotAPI.Stop()
    WalabotAPI.Disconnect()
    print ('Terminate successfully')
if __name__ == '__main__':
    InWallApp()