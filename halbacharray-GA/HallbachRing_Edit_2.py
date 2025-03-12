import matplotlib.pyplot as plt
import numpy as np

# Work in mm and use radii

class HallbachRing:
    def __init__(self, magnetSize=0.012, boreRadius=0.100, magnetRingRadii=[-1]*3, magnetsInRingNr=[-1]*3, bandGap = 0, magnetSpace = 0, bandSep = 0):

        # Primary function of this class is to check that all parameters work,
        # and throw an error should it not be the case.
        # Also show how many magnets can still be added etc.

        # User input to initiate:
        # Magnet Size
        # Bore size
        # Number of rings
        # Initiate array for individual magnet ring radii, magnet numbers of each. (Enter -1 to set to maximum)
        # Outer border is not so NB, but implement regardless

        self.magnetSize = magnetSize
        self.magnetRadius = self.calculateMagnetRadius(magnetSize)
        self.boreRadius = boreRadius
        self.bandGap = bandGap
        self.magnetSpace = magnetSpace
        self.magnetRing = []
        self.bandSep = bandSep

        for index, magnetRingRadius in enumerate(magnetRingRadii):
            self.magnetRing.append(self.createMagnetRing(index, magnetRingRadius, magnetsInRingNr[index], self.bandGap, self.bandSep))

        return None
    
    @classmethod
    def calculateMagnetRadius(self, magnetSize):
        # Note here radii are slightly larger than magnet.
        return round(np.sqrt(((magnetSize**2)/2)), 6)

    def calculateMaxMagnetNumber(self, magnetRadius, magnetRingRadius, magnetSpace):
        return round(np.pi/np.arcsin((self.magnetRadius + (magnetSpace/2))/magnetRingRadius))

    def calculateMagnetPositions(self, magnetNumber):
        # Returns magnet positions in radius distributed around a circle
        # If you use a max value, it might need to be rounded.
        return np.linspace(0, 2*np.pi, round(magnetNumber), endpoint = False)

    def createMagnetRing(self, index, magnetRingRadius, magnetsInRingNr, bandGap, bandSep):

        # Checks parameters and stores in a array of dictionaries if correct.

        if(index == 0):
            minimumRadius = self.boreRadius + self.magnetRadius + bandSep
        else:
            minimumRadius = self.magnetRing[index -1]['ringRadius']+self.magnetRadius*2 + bandGap

        if(magnetRingRadius == -1):
            magnetRingRadius = minimumRadius

        if(magnetRingRadius < minimumRadius):
            raise ValueError("magnetRing %d: magnetRing magnet radius of %.3fmm is too small. Minimum is %.3f" % (
                index, magnetRingRadius, minimumRadius))

        maxRingMagnetNr = self.calculateMaxMagnetNumber(
            self.magnetRadius, magnetRingRadius, self.magnetSpace)

        if(magnetsInRingNr == -1):

            magnetsInRingNr = maxRingMagnetNr

        elif(magnetsInRingNr > maxRingMagnetNr):
            raise ValueError("magnetRing %d: Can not fit %d magnets in a radius of %.3fmm. Max is %d"
                             % (index, magnetsInRingNr, magnetRingRadius, maxRingMagnetNr))

        aMagnetRing = {

            "ringRadius": magnetRingRadius,
            "magnetsInRingNr": magnetsInRingNr}

        return aMagnetRing

    def plotSingleRing(self, MagnetNumber, magnetRadius, ringRadius, ax):

        magnetTheta = self.calculateMagnetPositions(MagnetNumber)

        theta = np.arange(0, 2*np.pi, 150)

        for i in magnetTheta:

           # Calculate circle position
            x = ringRadius * np.cos(i)
            y = ringRadius * np.sin(i)

            # Draw the circle (magnet)
            circle1 = plt.Circle((x, y), magnetRadius, color='red', fill=False)
            ax.add_patch(circle1)

            # Calculate the dimensions of the square inside the circle
            square_side = self.magnetSize
            square_left = x - square_side / 2
            square_bottom = y - square_side / 2

            # Determine the rotation of the square (360 degrees for every 180 degrees around the ring)
            squareAngle = np.degrees(i) * 2

            # Draw the square inside the circle
            square = plt.Rectangle((square_left, square_bottom), square_side, square_side, angle = squareAngle, rotation_point = 'center',  edgecolor='blue', fill=False)
            ax.add_patch(square)

        innerCircle = plt.Circle((np.cos(theta), np.sin(
            theta)), ringRadius, color='red', linestyle='--', fill=False)
        ax.add_patch(innerCircle)

        plt.axis("equal")

        return ax

    def drawHallbach(self,fileName=""):

        fig, ax = plt.subplots()
        plt.grid()

        ax.set_xlim([-0.3,0.3])
        ax.set_ylim([-0.3,0.3])

        boreCircle = plt.Circle((0, 0), self.boreRadius,
                                color='black', fill=False)
        ax.add_patch(boreCircle)

        for i in range(len(self.magnetRing)):
            RingBorder = plt.Circle(
                (0, 0), self.magnetRing[i]['ringRadius']+self.magnetRadius, color='gray', linestyle='--', fill=False)
            ax.add_patch(RingBorder)
            ax = self.plotSingleRing(
                self.magnetRing[i]['magnetsInRingNr'], self.magnetRadius, self.magnetRing[i]['ringRadius'], ax)

        if (fileName != ""):
            plt.savefig(fileName)
            plt.close()
            print("Wrote %s" %(fileName))    
        else:
            plt.show()

        return ax


    def getParameters(self):

        ringRadii = np.empty(len(self.magnetRing))
        magnetsInRingNrs = np.empty(len(self.magnetRing))

        for i in range(len(self.magnetRing)):
            ringRadii[i] = self.magnetRing[i]['ringRadius']
            magnetsInRingNrs[i] = self.magnetRing[i]['magnetsInRingNr']

        return ringRadii, magnetsInRingNrs

