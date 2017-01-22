from geometry import Fuselage
from geometry import Wing
from geometry import Stabilizer
from geometry import Fin
from geometry import Nacelle

class Aerodynamics:
    
    def __init__(self, fuse, wing, stab, fin, nac):
        self.__fuse = fuse
        self.__wing = wing
        self.__stab = stab
        self.__fin  = fin
        self.__nac  = nac

    __liftToDrag = 20.0
    
    

    # MARK: print information

    def printInformation(self):
        print "Aerodynamics:"
        print "--------------------------------------"
        print "  L/D = %s" % self.__liftToDrag
        print ""
