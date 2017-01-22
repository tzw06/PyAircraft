import matplotlib.pyplot as plt
import seaborn as sns

import xlrd
import xml.dom.minidom
import string
import math

import sys,os  

class Fuselage:
    
    __name = "fuselage"
    
    # MARK: variables to be specified

    __length = 63
    __width  = 6
    __height = 6
    __lengthFront = 12
    __lengthMid = 0
    __lengthRear = 24
    
    __fuelTankVolume = 0
    
    # MARK: variables auto calculated

    __profile_x  = []
    __profile_yu = []
    __profile_yb = []
    __profile_z  = []
    
    # MARK: get variables
    
    def getDimension(self):
        return (self.__length, self.__width, self.__height)

    # MARK: geometry methods
    
    def setDimension(self, length, width, height):
        self.__length = length
        self.__width  = width
        self.__height = height
    
    def setLengthSection(self, length_f, length_r):
        self.__lengthFront = length_f
        self.__lengthRear = length_r
        self.__lengthMid = self.__length - length_f - length_r
    
    def setProfile(self, xs, yus, ybs, zs):
        self.__profile_x  = xs[:]
        self.__profile_yu = yus[:]
        self.__profile_yb = ybs[:]
        self.__profile_z  = zs[:]
    
    def calcWetArea(self):
        print "to be added"
    
    def getFuelTankVolume(self):
        return self.__fuelTankVolume
    
    # MARK: assembly
    
    def getOrigin(self):
        return (0,0,0)
    
    # MARK: input & output
    
    def open(self, filename):
        dom = xml.dom.minidom.parse(filename)
        root =  dom.documentElement
        fuseElement = root.getElementsByTagName('fuselage')[0]
        
        self.__length = string.atof(fuseElement.getElementsByTagName('length')[0].firstChild.data)
        self.__width  = string.atof(fuseElement.getElementsByTagName('width')[0].firstChild.data)
        self.__height = string.atof(fuseElement.getElementsByTagName('height')[0].firstChild.data)
        
        length_f = string.atof(fuseElement.getElementsByTagName('front-length')[0].firstChild.data)
        length_r = string.atof(fuseElement.getElementsByTagName('rear-length')[0].firstChild.data)
        self.setLengthSection(length_f, length_r)
        
        self.__fuelTankVolume = string.atof(fuseElement.getElementsByTagName('fuel-tank-volume')[0].firstChild.data)

        sectionElement = fuseElement.getElementsByTagName('section')[0]
        sectionName = sectionElement.firstChild.data
        filename = "profile/fuselage/" + sectionName

        self.__profile_x  = []
        self.__profile_yu = []
        self.__profile_yb = []
        self.__profile_z  = []

        with open(filename,'r') as f:
            for line in f:
                data = list(map(float,line.split(',')))
                self.__profile_x.append(data[0])
                self.__profile_yu.append(data[1]+data[3])
                self.__profile_yb.append(data[1]-data[4])
                self.__profile_z.append(data[2]+data[5])

    
    # MARK: print information
    
    def printInformation(self):
        print "Fuselage:"
        print "--------------------------------------"
        print "  Length = %s m" % self.__length
        print "  Width  = %s m" % self.__width
        print "  Height = %s m" % self.__height
        print ""

    # MARK: plot outline

    def plotProfile(self):
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        plt.sca(ax1)
        plt.plot(self.__profile_x, self.__profile_yu, 'r', self.__profile_x, self.__profile_yb, 'r')
        plt.sca(ax2)
        plt.plot(self.__profile_x, self.__profile_z)
        plt.show()

    def plotTopView(self, origin):
        length = self.__length
        width = self.__width
        
        x0 = origin[0]
        z0 = origin[1]
        
        xs = [x0+x*length for x in self.__profile_x]
        zp = [z0+z*width/2 for z in self.__profile_z]
        zm = [z0-z*width/2 for z in self.__profile_z]

        plt.plot(xs, zp, 'b', xs, zm, 'b')

    def plotSideView(self, origin):
        length = self.__length
        height = self.__height

        x0 = origin[0]
        y0 = origin[1]

        xs = [x0+x*length for x in self.__profile_x]
        yu = [y0+y*height/2 for y in self.__profile_yu]
        yb = [y0+y*height/2 for y in self.__profile_yb]

        plt.plot(xs, yu, 'b', xs, yb, 'b')


class Wing:

    __name = "wing"
    
    # MARK: variables to be specified
    
    __refArea = 388.0
    __aspectRatio = 9.6
    __sweptAngle = 32.0
    __taperRatio = 0.3
    __kinkPercent = 0.33
    
    __sweptTEin = 0
    
    __dihedral = 0
    
    __fuelTankVolume = 0
    
    __mountPercentOfX = 0
    __mountPercentOfY = 0
    
    # MARK: variables auto calculated
    
    __span = 1.0
    __rootChord = 1.0
    __kinkChord = 1.0
    __tipChord = 1.0
    __macLength = 1.0
    __macX = 1.0
    __macZ = 1.0
    
    __sweptAngleLE = 25.0
    __sweptAngleTE = 25.0
    
    __profile_z = []
    __profile_xle = []
    __profile_xte = []
    __profile_twist = []
    __profile_dihedral = []
    
    __airfoil_x = []
    __airfoil_yu = []
    __airfoil_yb = []
    
    # MARK: variables of other parts
    
    __fuseLength = 0
    __fuseWidth = 0
    __fuseHeight = 0
    __fuseX0 = 0
    __fuseY0 = 0
    __fuseZ0 = 0
    
    # MARK: get variables
    
    def getDimension(self):
        return (self.__rootChord, self.__span)

    def getProfile(self):
        return (self.__profile_z, self.__profile_xle, self.__profile_xte)

    # MARK: geometry methods
    
    def calcDimension(self):
        S = self.__refArea
        AR = self.__aspectRatio
        a = self.__fuseWidth / 2
        eta = self.__kinkPercent
        lmda = self.__taperRatio
    
        b = math.sqrt(S*AR)
    
        tmpA = (eta*b/2-a) * (b/2-a)
        tmpB = (1-lmda) * (0.75*eta*b/2+a/2) + (1+lmda)*b/2

        Cr = (S + tmpA * ( math.tan(self.__sweptAngle*math.pi/180.0) - math.tan(self.__sweptTEin*math.pi/180.0) ) ) / tmpB
        Ct = lmda * Cr
        
        tanLambdaLE = math.tan(self.__sweptAngle*math.pi/180) - (1-lmda)/2*Cr/(b-2*a)
        tanLambdaTE = math.tan(self.__sweptAngle*math.pi/180) + (1-lmda)/2*Cr/(b-2*a)
        
        Ck = Cr - (eta*b/2-a) * (tanLambdaLE-math.tan(self.__sweptTEin*math.pi/180))

        self.__span = b
        self.__rootChord = Cr
        self.__tipChord = Ct
        self.__kinkChord = Ck
        
        self.__sweptAngleLE = math.atan(tanLambdaLE) / math.pi * 180
        self.__sweptAngleTE = math.atan(tanLambdaTE) / math.pi * 180
    
        self.__profile_z  = [0, 2*a/b, eta, 1]
        self.__profile_xle = [0, 0, (eta*b/2-a)/Cr*tanLambdaLE, (b/2-a)/Cr*tanLambdaLE]
        self.__profile_xte = [1, 1, (eta*b/2-a)/Cr*tanLambdaLE+Ck/Cr, (b/2-a)/Cr*tanLambdaLE+lmda]
        self.__profile_twist = [0,0,0,0]
        self.__profile_dihedral = [6,6,6,6]

    
    def setFuselageParameters(self, fuseLength, fuseWidth, fuseHeight, fuseX0, fuseY0, fuseZ0):
        self.__fuseLength = fuseLength
        self.__fuseWidth = fuseWidth
        self.__fuseHeight = fuseHeight
        self.__fuseX0 = fuseX0
        self.__fuseY0 = fuseY0
        self.__fuseZ0 = fuseZ0

    def calcWetArea(self):
        print "to be added"
    
    def calcMeanAeroChord(self):
        nsec = len(self.__profile_z)
        sumS = 0
        sumC = 0
        sumX = 0
        sumZ = 0
        for isec in range(0,nsec-1):
            Cr = self.__rootChord
            sb = self.__span / 2
            
            Ca = Cr * ( self.__profile_xte[isec] - self.__profile_xle[isec] )
            Cb = Cr * ( self.__profile_xte[isec+1] - self.__profile_xle[isec+1] )
            Xb = Cr * ( self.__profile_xle[isec+1] - self.__profile_xle[isec] )
            Zb = sb * ( self.__profile_z[isec+1] - self.__profile_z[isec] )
            X0 = Cr * self.__profile_xle[isec]
            Z0 = sb * self.__profile_z[isec]
            
            Si = (Ca+Cb)*Zb/2
            Ci = (Cb+Ca*Ca/(Ca+Cb))*2/3
            Xi = (1+Cb/(Ca+Cb)) * Xb/3
            Zi = (1+Cb/(Ca+Cb)) * Zb/3
            
            sumC = sumC + Ci*Si
            sumX = sumX + (X0+Xi)*Si
            sumZ = sumZ + (Z0+Zi)*Si
            sumS = sumS + Si
        
        self.__macLength = sumC / sumS
        self.__macX = sumX / sumS
        self.__macZ = sumZ / sumS
    
    def getFuelTankVolume(self):
        return self.__fuelTankVolume
    
    # MARK: assembly
    
    def getOrigin(self):
        x0 = self.__fuseLength * self.__mountPercentOfX - self.__macX - 0.25*self.__macLength
        y0 = self.__fuseHeight * self.__mountPercentOfY
        return (x0+self.__fuseX0, y0+self.__fuseY0, self.__fuseZ0)
    
    # MARK: input & output
    
    def open(self, filename):
        dom = xml.dom.minidom.parse(filename)
        root =  dom.documentElement
        wingElement = root.getElementsByTagName('wing')[0]
        
        self.__refArea = string.atof(wingElement.getElementsByTagName('ref-area')[0].firstChild.data)
        self.__aspectRatio = string.atof(wingElement.getElementsByTagName('aspect-ratio')[0].firstChild.data)
        self.__sweptAngle = string.atof(wingElement.getElementsByTagName('swept-angle')[0].firstChild.data)
        self.__taperRatio = string.atof(wingElement.getElementsByTagName('taper-ratio')[0].firstChild.data)
        self.__kinkPercent = string.atof(wingElement.getElementsByTagName('kink-percent')[0].firstChild.data)
        
        self.__sweptTEin = string.atof(wingElement.getElementsByTagName('swept-angle-te-in')[0].firstChild.data)
        
        self.__dihedral = string.atof(wingElement.getElementsByTagName('dihedral')[0].firstChild.data)
        
        self.__fuelTankVolume = string.atof(wingElement.getElementsByTagName('fuel-tank-volume')[0].firstChild.data)
        
        self.__mountPercentOfX = string.atof(wingElement.getElementsByTagName('mount-percent-of-x')[0].firstChild.data)
        self.__mountPercentOfY = string.atof(wingElement.getElementsByTagName('mount-percent-of-y')[0].firstChild.data)
        
        self.calcDimension()
    
        airfoilElement = wingElement.getElementsByTagName('airfoil')[0]
        airfoilName = airfoilElement.firstChild.data
        filename = "profile/airfoil/" + airfoilName
    
        with open(filename,'r') as f:
            for line in f:
                data = list(map(float,line.split(',')))
                self.__airfoil_x.append(data[0])
                self.__airfoil_yu.append(data[1])
                self.__airfoil_yb.append(data[2])
    

    # MARK: print information

    def printInformation(self):
        print "Wing:"
        print "--------------------------------------"
        print "  Ref Area     = %s m^2" % self.__refArea
        print "  Aspect Ratio = %s"     % self.__aspectRatio
        print "  Swept Angle  = %s deg" % self.__sweptAngle
        print "  Taper Ratio  = %s"     % self.__taperRatio
        print "  Span         = %s m"   % self.__span
        print "  Root Chord   = %s"     % self.__rootChord
        print "  Kink Chord   = %s"     % self.__kinkChord
        print "  Tip Chord    = %s"     % self.__tipChord
        print "  MAC Length   = %s"     % self.__macLength
        print "  MAX X        = %s"     % self.__macX
        print "  MAX Z        = %s"     % self.__macZ
        print ""

    # MARK: plot outline

    def plotTopView(self, origin):
        Cr = self.__rootChord
        sb = self.__span / 2
        
        x0,y0,z0 = self.getOrigin()
        x0 = x0 + origin[0]
        z0 = z0 + origin[1]
        
        zls = [z0+z*sb for z in self.__profile_z]
        zrs = [z0-z*sb for z in self.__profile_z]
        xls = [x0+x*Cr for x in self.__profile_xle]
        xts = [x0+x*Cr for x in self.__profile_xte]
        
        plt.plot(xls, zls, 'b', xts, zls, 'b', xls, zrs, 'b', xts, zrs, 'b')
        
        nsec = len(self.__profile_z)
        xtip = [ x0 + Cr * self.__profile_xle[nsec-1], x0 + Cr * self.__profile_xte[nsec-1] ]
        zltip = [ z0 + sb * self.__profile_z[nsec-1], z0 + sb * self.__profile_z[nsec-1] ]
        zrtip = [ z0 - sb * self.__profile_z[nsec-1], z0 - sb * self.__profile_z[nsec-1] ]
        
        plt.plot(xtip, zltip, 'b', xtip, zrtip, 'b')
        
        macxs = [x0+self.__macX, x0+self.__macX+self.__macLength]
        maczs = [z0+self.__macZ, z0+self.__macZ]
        
        plt.plot(macxs, maczs, 'r')

    def plotSideView(self, origin):
        Cr = self.__rootChord
        Ct = self.__tipChord
        sb = self.__span / 2

        tanD = math.tan(self.__dihedral*math.pi/180)

        x0,y0,z0 = self.getOrigin()
        x0 = x0 + origin[0]
        y0 = y0 + origin[1]

        xls = [x0+x*Cr for x in self.__profile_xle[1:4]]
        xts = [x0+x*Cr for x in self.__profile_xte[1:4]]
        ys = [y0+z*sb*tanD for z in self.__profile_z[1:4]]

        plt.plot(xls, ys, 'b', xts, ys, 'b', linewidth=1)

        af_xs = [x0+Cr*xi for xi in self.__airfoil_x]
        af_yus = [y0+Cr*et for et in self.__airfoil_yu]
        af_ybs = [y0+Cr*et for et in self.__airfoil_yb]

        plt.plot(af_xs, af_yus, 'b', af_xs, af_ybs, 'b', linewidth=1)

        xt = x0 + Cr * self.__profile_xle[3]
        yt = y0 + sb * tanD

        af_xs = [xt+Ct*xi for xi in self.__airfoil_x]
        af_yus = [yt+Ct*et for et in self.__airfoil_yu]
        af_ybs = [yt+Ct*et for et in self.__airfoil_yb]

        plt.plot(af_xs, af_yus, 'b', af_xs, af_ybs, 'b', linewidth=1)


class Stabilizer:

    __name = "stabilizer"
    
    # MARK: variables to be specified

    __refArea = 80.0
    __aspectRatio = 5.0
    __sweptAngle = 25.0
    __taperRatio = 0.3
    __thickness = 0.1
    
    __dihedral = 0
    
    __mountPercentOfX = 0
    __mountPercentOfY = 0
    
    # MARK: variables auto calculated

    __span = 1.0
    __rootChord = 1.0
    __tipChord = 1.0
    __macLength = 1.0
    __macX = 1.0
    __macZ = 1.0

    __sweptAngleLE = 25.0
    __sweptAngleMid = 25.0
    
    __profile_z = []
    __profile_xle = []
    __profile_xte = []
    __profile_twist = []
    __profile_dihedral = []
    
    # MARK: variables of other parts
    
    __fuseLength = 0
    __fuseWidth = 0
    __fuseHeight = 0
    __fuseX0 = 0
    __fuseY0 = 0
    __fuseZ0 = 0

    # MARK: geometry methods

    def calcDimension(self):
        S = self.__refArea
        AR = self.__aspectRatio
        lmda = self.__taperRatio
    
        b = math.sqrt(S*AR)
        Cr = 2*S/b/(1+lmda)
        Ct = Cr * lmda
        
        tanLambdaLE = math.tan(self.__sweptAngle*math.pi/180) + Cr/2/b*(1-lmda)
        tanLambdaMid = math.tan(self.__sweptAngle*math.pi/180) - Cr/2/b*(1-lmda)
        
        self.__span = b
        self.__rootChord = Cr
        self.__tipChord = Ct
        self.__sweptAngleLE = math.atan(tanLambdaLE) * 180 / math.pi
        self.__sweptAngleMid = math.atan(tanLambdaMid) * 180 / math.pi
    
        self.__profile_z = [0,1]
        self.__profile_xle = [0, (1-lmda)/4 + b/2/Cr*math.tan(self.__sweptAngle*math.pi/180)]
        self.__profile_xte = [1, (1-lmda)/4 + b/2/Cr*math.tan(self.__sweptAngle*math.pi/180) + lmda]
        self.__profile_twist = [0,0]
        self.__profile_dihedral = [6,6]
    
    def setFuselageParameters(self, fuseLength, fuseWidth, fuseHeight, fuseX0, fuseY0, fuseZ0):
        self.__fuseLength = fuseLength
        self.__fuseWidth = fuseWidth
        self.__fuseHeight = fuseHeight
        self.__fuseX0 = fuseX0
        self.__fuseY0 = fuseY0
        self.__fuseZ0 = fuseZ0
    
    def calcWetArea(self):
        print "to be added"
    
    def calcMeanAeroChord(self):
        nsec = len(self.__profile_z)    
        sumS = 0
        sumC = 0
        sumX = 0
        sumZ = 0
        for isec in range(0,nsec-1):
            Cr = self.__rootChord
            sb = self.__span / 2
            
            Ca = Cr * ( self.__profile_xte[isec] - self.__profile_xle[isec] )
            Cb = Cr * ( self.__profile_xte[isec+1] - self.__profile_xle[isec+1] )
            Xb = Cr * ( self.__profile_xle[isec+1] - self.__profile_xle[isec] )
            Zb = sb * ( self.__profile_z[isec+1] - self.__profile_z[isec] )
            X0 = Cr * self.__profile_xle[isec]
            Z0 = sb * self.__profile_z[isec]
            
            Si = (Ca+Cb)*Zb/2
            Ci = (Cb+Ca*Ca/(Ca+Cb))*2/3
            Xi = (1+Cb/(Ca+Cb)) * Xb/3
            Zi = (1+Cb/(Ca+Cb)) * Zb/3

            sumC = sumC + Ci*Si
            sumX = sumX + (X0+Xi)*Si
            sumZ = sumZ + (Z0+Zi)*Si
            sumS = sumS + Si
            
        self.__macLength = sumC / sumS
        self.__macX = sumX / sumS
        self.__macZ = sumZ / sumS

    # MARK: assembly

    def getOrigin(self):
        x0 = self.__fuseLength * self.__mountPercentOfX - self.__macX - 0.25*self.__macLength
        y0 = self.__fuseHeight * self.__mountPercentOfY
        return (x0+self.__fuseX0, y0+self.__fuseY0, self.__fuseZ0)

    # MARK: input & output
    
    def open(self, filename):
        dom = xml.dom.minidom.parse(filename)
        root =  dom.documentElement
        stabElement = root.getElementsByTagName('stabilizer')[0]

        self.__refArea = string.atof(stabElement.getElementsByTagName('ref-area')[0].firstChild.data)
        self.__aspectRatio = string.atof(stabElement.getElementsByTagName('aspect-ratio')[0].firstChild.data)
        self.__sweptAngle = string.atof(stabElement.getElementsByTagName('swept-angle')[0].firstChild.data)
        self.__taperRatio = string.atof(stabElement.getElementsByTagName('taper-ratio')[0].firstChild.data)

        self.__dihedral = string.atof(stabElement.getElementsByTagName('dihedral')[0].firstChild.data)

        self.__mountPercentOfX = string.atof(stabElement.getElementsByTagName('mount-percent-of-x')[0].firstChild.data)
        self.__mountPercentOfY = string.atof(stabElement.getElementsByTagName('mount-percent-of-y')[0].firstChild.data)
        
        self.calcDimension()

    # MARK: print information

    def printInformation(self):
        print "Stabilizer:"
        print "--------------------------------------"
        print "  Ref Area     = %s m^2" % self.__refArea
        print "  Aspect Ratio = %s"     % self.__aspectRatio
        print "  Swept Angle  = %s deg" % self.__sweptAngle
        print "  Taper Ratio  = %s"     % self.__taperRatio
        print "  Span         = %s m"   % self.__span
        print "  Root Chord   = %s"     % self.__rootChord
        print "  Tip Chord    = %s"     % self.__tipChord
        print "  MAC Length   = %s"     % self.__macLength
        print "  MAX X        = %s"     % self.__macX
        print "  MAX Z        = %s"     % self.__macZ
        print ""

    # MARK: plot outline

    def plotTopView(self, origin):
        Cr = self.__rootChord
        sb = self.__span / 2
        
        x0,y0,z0 = self.getOrigin()
        x0 = x0 + origin[0]
        z0 = z0 + origin[1]
        
        zls = [z0+z*sb for z in self.__profile_z]
        zrs = [z0-z*sb for z in self.__profile_z]
        xls = [x0+x*Cr for x in self.__profile_xle]
        xts = [x0+x*Cr for x in self.__profile_xte]
    
        plt.plot(xls, zls, 'b', xts, zls, 'b', xls, zrs, 'b', xts, zrs, 'b')
        
        nsec = len(self.__profile_z)
        xtip = [ x0 + Cr * self.__profile_xle[nsec-1], x0 + Cr * self.__profile_xte[nsec-1] ]
        zltip = [ z0 + sb * self.__profile_z[nsec-1], z0 + sb * self.__profile_z[nsec-1] ]
        zrtip = [ z0 - sb * self.__profile_z[nsec-1], z0 - sb * self.__profile_z[nsec-1] ]
        
        plt.plot(xtip, zltip, xtip, zrtip, 'b')
    
        macxs = [x0+self.__macX, x0+self.__macX+self.__macLength]
        maczs = [z0+self.__macZ, z0+self.__macZ]
        
        plt.plot(macxs, maczs, 'r')

    def plotSideView(self, origin):
        Cr = self.__rootChord
        sb = self.__span / 2
        
        tanD = math.tan(self.__dihedral*math.pi/180)
        
        x0,y0,z0 = self.getOrigin()
        x0 = x0 + origin[0]
        y0 = y0 + origin[1]
        
        xls = [x0+x*Cr for x in self.__profile_xle]
        xts = [x0+x*Cr for x in self.__profile_xte]
        ys = [y0+z*sb*tanD for z in self.__profile_z]
        
        plt.plot(xls, ys, 'b', xts, ys, 'b', linewidth=1)

class Fin:

    __name = "fin"
    
    # MARK: variables to be specified

    __refArea = 40.0
    __aspectRatio = 1.6
    __sweptAngle = 25.0
    __taperRatio = 0.3
    
    __mountPercentOfX = 0
    __mountPercentOfY = 0
    
    # MARK: variables auto calculated
    
    __span = 1.0
    __rootChord = 1.0
    __tipChord = 1.0
    __macLength = 1.0
    __macX = 1.0
    __macY = 1.0
    
    __sweptAngleLE = 25.0
    __sweptAngleMid = 25.0
    
    __profile_y = []
    __profile_xle = []
    __profile_xte = []

    # MARK: variables of other parts

    __fuseLength = 0
    __fuseWidth = 0
    __fuseHeight = 0
    __fuseX0 = 0
    __fuseY0 = 0
    __fuseZ0 = 0
    
    # MARK: geometry methods

    def calcDimension(self):
        S = self.__refArea
        AR = self.__aspectRatio
        lmda = self.__taperRatio
        
        b = math.sqrt(S*AR)
        Cr = 2*S/b/(1+lmda)
        Ct = Cr * lmda
        
        tanLambdaLE = math.tan(self.__sweptAngle*math.pi/180) + Cr/2/b*(1-lmda)
        tanLambdaMid = math.tan(self.__sweptAngle*math.pi/180) - Cr/2/b*(1-lmda)
        
        self.__span = b
        self.__rootChord = Cr
        self.__tipChord = Ct
        self.__sweptAngleLE = math.atan(tanLambdaLE) * 180 / math.pi
        self.__sweptAngleMid = math.atan(tanLambdaMid) * 180 / math.pi
        
        self.__profile_y = [0,1]
        self.__profile_xle = [0, (1-lmda)/4 + b/2/Cr*math.tan(self.__sweptAngle*math.pi/180)]
        self.__profile_xte = [1, (1-lmda)/4 + b/2/Cr*math.tan(self.__sweptAngle*math.pi/180) + lmda]

    def setFuselageParameters(self, fuseLength, fuseWidth, fuseHeight, fuseX0, fuseY0, fuseZ0):
        self.__fuseLength = fuseLength
        self.__fuseWidth = fuseWidth
        self.__fuseHeight = fuseHeight
        self.__fuseX0 = fuseX0
        self.__fuseY0 = fuseY0
        self.__fuseZ0 = fuseZ0
    
    def calcWetArea(self):
        print "to be added"

    def calcMeanAeroChord(self):
        nsec = len(self.__profile_y)
        sumS = 0
        sumC = 0
        sumX = 0
        sumY = 0
        for isec in range(0,nsec-1):
            Cr = self.__rootChord
            b = self.__span
            
            Ca = Cr * ( self.__profile_xte[isec] - self.__profile_xle[isec] )
            Cb = Cr * ( self.__profile_xte[isec+1] - self.__profile_xle[isec+1] )
            Xb = Cr * ( self.__profile_xle[isec+1] - self.__profile_xle[isec] )
            Yb = b * ( self.__profile_y[isec+1] - self.__profile_y[isec] )
            X0 = Cr * self.__profile_xle[isec]
            Y0 = b * self.__profile_y[isec]
            
            Si = (Ca+Cb)*Yb/2
            Ci = (Cb+Ca*Ca/(Ca+Cb))*2/3
            Xi = (1+Cb/(Ca+Cb)) * Xb/3
            Yi = (1+Cb/(Ca+Cb)) * Yb/3
            
            sumC = sumC + Ci*Si
            sumX = sumX + (X0+Xi)*Si
            sumY = sumY + (Y0+Yi)*Si
            sumS = sumS + Si
        
        self.__macLength = sumC / sumS
        self.__macX = sumX / sumS
        self.__macY = sumY / sumS


    # MARK: assembly

    def getOrigin(self):
        x0 = self.__fuseLength * self.__mountPercentOfX - self.__macX - 0.25*self.__macLength
        y0 = self.__fuseHeight * self.__mountPercentOfY
        return (x0+self.__fuseX0, y0+self.__fuseY0, self.__fuseZ0)
    
    # MARK: input & output

    def open(self, filename):
        dom = xml.dom.minidom.parse(filename)
        root =  dom.documentElement
        finElement = root.getElementsByTagName('fin')[0]
        
        self.__refArea = string.atof(finElement.getElementsByTagName('ref-area')[0].firstChild.data)
        self.__aspectRatio = string.atof(finElement.getElementsByTagName('aspect-ratio')[0].firstChild.data)
        self.__sweptAngle = string.atof(finElement.getElementsByTagName('swept-angle')[0].firstChild.data)
        self.__taperRatio = string.atof(finElement.getElementsByTagName('taper-ratio')[0].firstChild.data)
        
        self.__mountPercentOfX = string.atof(finElement.getElementsByTagName('mount-percent-of-x')[0].firstChild.data)
        self.__mountPercentOfY = string.atof(finElement.getElementsByTagName('mount-percent-of-y')[0].firstChild.data)
        
        self.calcDimension()

    # MARK: print information

    def printInformation(self):
        print "Fin:"
        print "--------------------------------------"
        print "  Ref Area = %s m^2"     % self.__refArea
        print "  Aspect Ratio = %s"     % self.__aspectRatio
        print "  Swept Angle  = %s deg" % self.__sweptAngle
        print "  Taper Ratio  = %s"     % self.__taperRatio
        print "  Span         = %s m"   % self.__span
        print "  Root Chord   = %s"     % self.__rootChord
        print "  Tip Chord    = %s"     % self.__tipChord
        print "  MAC Length   = %s"     % self.__macLength
        print "  MAX X        = %s"     % self.__macX
        print "  MAX Y        = %s"     % self.__macY
        print ""

    # MARK: plot outline

    def plotSideView(self,origin):
        Cr = self.__rootChord
        b = self.__span
        
        x0,y0,z0 = self.getOrigin()
        x0 = x0 + origin[0]
        y0 = y0 + origin[1]
        
        ys = [y0+y*b for y in self.__profile_y]
        xls = [x0+x*Cr for x in self.__profile_xle]
        xts = [x0+x*Cr for x in self.__profile_xte]
        
        plt.plot(xls, ys, 'b', xts, ys, 'b')
        
        nsec = len(self.__profile_y)
        xtip = [ x0 + Cr * self.__profile_xle[nsec-1], x0 + Cr * self.__profile_xte[nsec-1] ]
        ytip = [ y0 + b * self.__profile_y[nsec-1], y0 + b * self.__profile_y[nsec-1] ]
        
        plt.plot(xtip, ytip, 'b')
        
        macxs = [x0+self.__macX, x0+self.__macX+self.__macLength]
        macys = [y0+self.__macY, y0+self.__macY]
        
        plt.plot(macxs, macys, 'r')


class Nacelle:

    __name = "nacelle"
    
    # MARK: variables to be specified

    __length = 4.0
    __width  = 3.0
    __height = 3.0
    
    __mountPercentOfZ = 0.33
    __dxToChord = 0.1
    __dyToChord = 0.1

    # MARK: variables auto calculated

    __profile_x  = []
    __profile_yu = []
    __profile_yb = []
    __profile_z  = []
    
    # MARK: variables of other parts
    
    __wingSpan = 0
    __wingRootChord = 0
    __wingX0 = 0
    __wingY0 = 0
    __wingZ0 = 0
    
    __wingProfile_z = []
    __wingProfile_xle = []
    __wingProfile_xte = []
    
    # MARK: geometry methods

    def setDimension(self, length, width, height):
        self.__length = length
        self.__width  = width
        self.__height = height
    
    def setWingParameters(self, wingRootChord, wingSpan, wingX0, wingY0, wingZ0):
        self.__wingSpan = wingSpan
        self.__wingRootChord = wingRootChord
        self.__wingX0 = wingX0
        self.__wingY0 = wingY0
        self.__wingZ0 = wingZ0
    
    def setWingProfile(self, zs, xles, xtes):
        self.__wingProfile_z = zs[:]
        self.__wingProfile_xle = xles[:]
        self.__wingProfile_xte = xtes[:]

    def calcWetArea(self):
        print "to be added"
    
    # MARK: assembly
    
    def getOrigin(self):
        
        zeta = self.__mountPercentOfZ
        xle = self.__wingProfile_xle[0]
        xte = self.__wingProfile_xte[0]
        yle = 0
        nsec = len(self.__wingProfile_z)
        for isec in range(1,nsec):
            z0 = self.__wingProfile_z[isec-1]
            z1 = self.__wingProfile_z[isec]
            if ( (zeta>=z0) and (zeta<z1) ):
                p = (zeta-z0)/(z1-z0)
                xle0 = self.__wingProfile_xle[isec-1]
                xte0 = self.__wingProfile_xte[isec-1]
                xle1 = self.__wingProfile_xle[isec]
                xte1 = self.__wingProfile_xte[isec]
                xle = (1-p) * xle0 + p * xle1
                xte = (1-p) * xte0 + p * xte1
                break;
    
        nsec = len(self.__profile_yu)
        dy = self.__profile_yu[nsec-1] * self.__height / 2
    
        c = xte - xle
        x0 = self.__wingRootChord * ( xle - c*self.__dxToChord ) - self.__length
        y0 = yle - self.__wingRootChord * c * self.__dyToChord - dy
        z0 = self.__wingSpan/2 * self.__mountPercentOfZ
        return (x0+self.__wingX0, y0+self.__wingY0, z0+self.__wingZ0)
    
    # MARK: input & output
    
    def open(self, filename):
        dom = xml.dom.minidom.parse(filename)
        root =  dom.documentElement
        nacElement = root.getElementsByTagName('nacelle')[0]
        
        self.__length = string.atof(nacElement.getElementsByTagName('length')[0].firstChild.data)
        self.__width  = string.atof(nacElement.getElementsByTagName('width')[0].firstChild.data)
        self.__height = string.atof(nacElement.getElementsByTagName('height')[0].firstChild.data)
        
        self.__mountPercentOfZ = string.atof(nacElement.getElementsByTagName('mount-percent-of-z')[0].firstChild.data)
        self.__dxToChord = string.atof(nacElement.getElementsByTagName('dx-to-chord')[0].firstChild.data)
        self.__dyToChord = string.atof(nacElement.getElementsByTagName('dy-to-chord')[0].firstChild.data)
        
        sectionElement = nacElement.getElementsByTagName('section')[0]
        sectionName = sectionElement.firstChild.data
        filename = "profile/nacelle/" + sectionName
        
        self.__profile_x  = []
        self.__profile_yu = []
        self.__profile_yb = []
        self.__profile_z  = []
        
        with open(filename,'r') as f:
            for line in f:
                data = list(map(float,line.split(',')))
                self.__profile_x.append(data[0])
                self.__profile_yu.append(data[1]+data[3])
                self.__profile_yb.append(data[1]-data[4])
                self.__profile_z.append(data[2]+data[5])

    
    # MARK: print information

    def printInformation(self):
        print "Nacelle:"
        print "--------------------------------------"
        print "  Length = %s m" % self.__length
        print "  Width  = %s m" % self.__width
        print "  Height = %s m" % self.__height
        print ""
    
    def plotProfile(self):
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        plt.sca(ax1)
        plt.plot(self.__profile_x, self.__profile_yu, 'r', self.__profile_x, self.__profile_yb, 'r')
        plt.sca(ax2)
        plt.plot(self.__profile_x, self.__profile_z)
        plt.show()
    
    def plotTopView(self, origin):
        length = self.__length
        width = self.__width
        
        x0,y0,z0 = self.getOrigin()
        x0 = x0 + origin[0]
        z0 = z0 + origin[1]

        xs = [x0+x*length for x in self.__profile_x]
        zp = [z0+z*width/2 for z in self.__profile_z]
        zm = [z0-z*width/2 for z in self.__profile_z]
        
        zp1 = [2*(self.__wingZ0+origin[1])-z for z in zp]
        zm1 = [2*(self.__wingZ0+origin[1])-z for z in zm]
        
        plt.plot(xs, zp, 'b', xs, zm, 'b', xs, zp1, 'b', xs, zm1, 'b')
    
        nsec = len(self.__profile_z)
        xl = [x0,x0]
        xe = [x0+length, x0+length]
        zl = [z0+self.__profile_z[0]*width/2, z0-self.__profile_z[0]*width/2]
        ze = [z0+self.__profile_z[nsec-1]*width/2, z0-self.__profile_z[nsec-1]*width/2]
    
        zl1 = [2*(self.__wingZ0+origin[1])-z for z in zl]
        ze1 = [2*(self.__wingZ0+origin[1])-z for z in ze]
    
        plt.plot(xl, zl, 'b', xe, ze, 'b', xl, zl1, 'b', xe, ze1, 'b')
    
    def plotSideView(self, origin):
        length = self.__length
        height = self.__height
        
        x0,y0,z0 = self.getOrigin()
        
        x0 = x0 + origin[0]
        y0 = y0 + origin[1]
        
        xs = [x0+x*length for x in self.__profile_x]
        yu = [y0+y*height/2 for y in self.__profile_yu]
        yb = [y0+y*height/2 for y in self.__profile_yb]
        
        plt.plot(xs, yu, 'b', xs, yb, 'b')

        nsec = len(self.__profile_z)
        xl = [x0,x0]
        xe = [x0+length, x0+length]
        yl = [y0+self.__profile_yu[0]*height/2, y0+self.__profile_yb[0]*height/2]
        ye = [y0+self.__profile_yu[nsec-1]*height/2, y0+self.__profile_yb[nsec-1]*height/2]

        plt.plot(xl, yl, 'b', xe, ye, 'b')
