class Mass:

    __MTOW = 234000
    __MLW  = 189000
    __MZFW = 185000
    __OEW  = 127600

    # MARK: print information

    def printInformation(self):
        print "Weight:"
        print "--------------------------------------"
        print "  MTOW = %s kg" % self.__MTOW
        print "  MLW  = %s kg" % self.__MLW
        print "  MZFW = %s kg" % self.__MZFW
        print "  OEW  = %s kg" % self.__OEW
        print ""