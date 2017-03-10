#!/usr/bin/python
import sys
import numpy as np

from aircraft import Aircraft
from geometry import Fuselage


print sys.argv

aircraft = Aircraft()
aircraft.open('aircraft20170309.xml')
aircraft.estimate()

for param in sys.argv:
    if param=="report":
        aircraft.printInformation()
    
    elif param=="outline":
        aircraft.plotOutline()

    elif param=="fuel tank volume":
        aircraft.calcFuelTankVolume()
