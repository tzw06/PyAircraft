#!/usr/bin/python
import os,sys
import numpy as np

from aircraft import Aircraft
#from geometry import Fuselage

print os.getcwd()

inputfile = ""
outputfile = ""
respath = sys.path[0] + "/../workspace"

try:
    i = sys.argv.index('-i')
    inputfile = sys.argv[i+1]
except:
    print "failed to assign input file"

try:
    i = sys.argv.index('-o')
    outputfile = sys.argv[i+1]
except:
    print "failed to assign output file"


if inputfile!="" and outputfile!="":
    
    aircraft = Aircraft(respath)
    aircraft.open(inputfile)
#        aircraft.open('aircraft20170309.xml')
    aircraft.estimate()

    for param in sys.argv:
        if param=="report":
            aircraft.printInformation()

        elif param=="outline":
            aircraft.plotOutline()

        elif param=="fuel tank volume":
            aircraft.calcFuelTankVolume()

    aircraft.save(inputfile, outputfile)
    


