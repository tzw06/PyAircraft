import os
import matplotlib.pyplot as plt
import seaborn as sns

from geometry import Fuselage
from geometry import Wing
from geometry import Stabilizer
from geometry import Fin
from geometry import Nacelle

from weight       import Mass
from aerodynamics import Aerodynamics
from performance  import Mission

class Aircraft:
    
    def __init__(self, respath):

        __name = "Default Aircraft"

        self.__respath = respath
        self.__fuse = Fuselage(respath)
        self.__wing = Wing(respath)
        self.__stab = Stabilizer(respath)
        self.__fin  = Fin(respath)
        self.__nac  = Nacelle(respath)
        
        self.__mass = Mass()
        self.__aero = Aerodynamics(self.__fuse, self.__wing, self.__stab, self.__fin, self.__nac)
        self.__mission    = Mission()
        self.__missionOff = Mission()
    
    # MARK: input & output
    
#    os.chdir("/Users/tzw/SDK/PyAircraft/workspace")

    def open(self, filename):
        print "load data from file: %s" % filename

        self.__fuse.open(filename)

        x0,y0,z0 = self.__fuse.getOrigin()
        fuseLength,fuseWidth,fuseHeight = self.__fuse.getDimension()
        self.__wing.setFuselageParameters(fuseLength, fuseWidth, fuseHeight, x0, y0, z0)
        self.__stab.setFuselageParameters(fuseLength, fuseWidth, fuseHeight, x0, y0, z0)
        self.__fin.setFuselageParameters(fuseLength, fuseWidth, fuseHeight, x0, y0, z0)
        
        self.__wing.open(filename)
        self.__stab.open(filename)
        self.__fin.open(filename)
        
        self.__wing.calcMeanAeroChord()
        self.__stab.calcMeanAeroChord()
        self.__fin.calcMeanAeroChord()
        
        x0,y0,z0 = self.__wing.getOrigin()
        zs,xles,xtes = self.__wing.getProfile()
        wingRootChord,wingSpan = self.__wing.getDimension()
        self.__nac.setWingParameters(wingRootChord, wingSpan, x0, y0, z0)
        self.__nac.setWingProfile(zs,xles,xtes)
        
        self.__nac.open(filename)
    
    def save(self, filename):
        print "save data to file: %s" % filename
        print "to be added"
    
    # MARK: calculation
    
    def estimate(self):
        print "estimating...\nto be modified"
        self.calcFuelTankVolume()
        self.__wing.calcMeanAeroChord()
        self.__stab.calcMeanAeroChord()
        self.__fin.calcMeanAeroChord()
    
    # MARK: methods
    
    def calcTailVolume(self):
        print "to be added"
    
    def calcWetArea(self):
        self.__fuse.calcWetArea()
        self.__wing.calcWetArea()
        self.__stab.calcWetArea()
        self.__fin.calcWetArea()
        self.__nac.calcWetArea()
    
    def calcFuelTankVolume(self):
        fuelTankVolume = self.__fuse.getFuelTankVolume() + self.__wing.getFuelTankVolume()
        print "Fuel Tank Volume = %s" % fuelTankVolume
    
    # MARK: print information
    
    def printInformation(self):
        self.__fuse.printInformation()
        self.__wing.printInformation()
        self.__stab.printInformation()
        self.__fin.printInformation()
        self.__nac.printInformation()
        self.__mass.printInformation()
        self.__aero.printInformation()
        self.__mission.printInformation()
    
    # MARK: plot outline
    
    def plotOutline(self):
        self.plotSideView([0,40])
        self.plotTopView([0,0])
        plt.axis("equal")
        plt.show()

    def plotTopView(self, origin):
        self.__fuse.plotTopView(origin)
        self.__wing.plotTopView(origin)
        self.__stab.plotTopView(origin)
        self.__nac.plotTopView(origin)
    
    def plotSideView(self, origin):
        self.__fuse.plotSideView(origin)
        self.__wing.plotSideView(origin)
        self.__stab.plotSideView(origin)
        self.__fin.plotSideView(origin)
        self.__nac.plotSideView(origin)
    
    
    # MARK: get components
    
    def getFuselage(self):
        return self.__fuse
    
    def getWing(self):
        return self.__wing
    
    def getStabilizer(self):
        return self.__stab
    
    def getFin(self):
        return self.__fin
    
    def getNacelle(self):
        return self.__nac

    # MARK: get features
    
    def getMass(self):
        return self.__mass

    def getAerodynamics(self):
        return self.__aero

    def getMission(self):
        return self.__mission

    def getMissionOff(self):
        return self.__missionOff



