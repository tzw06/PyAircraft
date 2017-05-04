#!/usr/bin/python
import os,sys
import numpy as np

from aircraft import Aircraft
#from geometry import Fuselage

print os.getcwd()

if '-i' in sys.argv:
    i = sys.argv.index('-i')

#    filename = os.getcwd() + '/' + sys.argv[i+1]
    filename = sys.argv[i+1]
    respath = sys.path[0] + "/../workspace"
    
    aircraft = Aircraft(respath)
    aircraft.open(filename)
#        aircraft.open('aircraft20170309.xml')
    aircraft.estimate()

    for param in sys.argv:
        if param=="report":
            aircraft.printInformation()

        elif param=="outline":
            aircraft.plotOutline()

        elif param=="fuel tank volume":
            aircraft.calcFuelTankVolume()
    


