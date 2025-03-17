import matplotlib.pyplot as plt
import numpy as np

# Work in mm and use radii

class HallbachRing:
    def __init__(self, magnetSize=0.012, boreRadius=0.100, magnetRingRadii=[-1]*3, magnetsInRingNr=[-1]*3, bandGap = 0, magnetSpace = 0, bandSep = 0):

        """
        Initializes a Halbach ring with given parameters.

        Parameters:
        - magnetSize (float): The size of the magnets (assumed to be square in cross-section).
        - boreRadius (float): The inner bore radius of the ring.
        - magnetRingRadii (list): A list of radii for each magnet ring. If -1, the radius is automatically assigned.
        - magnetsInRingNr (list): A list of magnet counts per ring. If -1, the maximum possible magnets are used.
        - bandGap (float): The gap between different bands of magnets.
        - magnetSpace (float): The spacing between adjacent magnets in a ring.
        - bandSep (float): The separation distance from the bore to the first ring.

        This function initializes the Halbach ring structure by creating magnet rings with valid configurations.
        """

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
        """
        Calculates the effective radius of a square magnet.

        Parameters:
        - magnetSize (float): The size of the square magnet.

        Returns:
        - float: The calculated radius of the magnet.
        """
        # Note here radii are slightly larger than magnet.
        return round(np.sqrt(((magnetSize**2)/2)), 6)

    def calculateMaxMagnetNumber(self, magnetRadius, magnetRingRadius, magnetSpace):
        """
        Calculates the maximum number of magnets that can fit around a given ring.

        Parameters:
        - magnetRadius (float): The radius of an individual magnet.
        - magnetRingRadius (float): The radius of the magnet ring.
        - magnetSpace (float): The spacing between adjacent magnets.

        Returns:
        - int: The maximum number of magnets that can fit in the ring.
        """
        return round(np.pi/np.arcsin((self.magnetRadius + (magnetSpace/2))/magnetRingRadius))

    def calculateMagnetPositions(self, magnetNumber):
        """
        Computes the angular positions of magnets around the ring.

        Parameters:
        - magnetNumber (int): Number of magnets in the ring.

        Returns:
        - np.ndarray: Array of angular positions (radians) for the magnets.
        """
        # Returns magnet positions in radius distributed around a circle
        # If you use a max value, it might need to be rounded.
        return np.linspace(0, 2*np.pi, round(magnetNumber), endpoint = False)

    def createMagnetRing(self, index, magnetRingRadius, magnetsInRingNr, bandGap, bandSep):
        """
        Creates a dictionary representing a single magnet ring with valid parameters.

        Parameters:
        - index (int): The index of the ring (starting from 0).
        - magnetRingRadius (float): The radius of the magnet ring. If -1, a minimum valid radius is assigned.
        - magnetsInRingNr (int): The number of magnets in the ring. If -1, the maximum possible number is used.
        - bandGap (float): The gap between different magnet bands.
        - bandSep (float): The separation distance from the bore to the first ring.

        Returns:
        - dict: A dictionary containing the ring radius and the number of magnets in the ring.

        Raises:
        - ValueError: If the provided ring radius is too small or if the requested number of magnets exceeds the maximum capacity.
        """
        
        # Determine the minimum valid radius for the ring
        if(index == 0):
            minimumRadius = self.boreRadius + self.magnetRadius + bandSep
        else:
            minimumRadius = self.magnetRing[index -1]['ringRadius']+self.magnetRadius*2 + bandGap

        # Assign minimum radius if not specified
        if(magnetRingRadius == -1):
            magnetRingRadius = minimumRadius

        # Check if the given radius is too small
        if(magnetRingRadius < minimumRadius):
            raise ValueError("magnetRing %d: magnetRing magnet radius of %.3fmm is too small. Minimum is %.3f" % (
                index, magnetRingRadius, minimumRadius))

        # Calculate the maximum number of magnets that can fit in this ring
        maxRingMagnetNr = self.calculateMaxMagnetNumber(
            self.magnetRadius, magnetRingRadius, self.magnetSpace)

        # Assign maximum number of magnets if not specified
        if(magnetsInRingNr == -1):

            magnetsInRingNr = maxRingMagnetNr

        elif(magnetsInRingNr > maxRingMagnetNr):
            raise ValueError("magnetRing %d: Can not fit %d magnets in a radius of %.3fmm. Max is %d"
                             % (index, magnetsInRingNr, magnetRingRadius, maxRingMagnetNr))

        aMagnetRing = {

            "ringRadius": magnetRingRadius,
            "magnetsInRingNr": magnetsInRingNr}

        return aMagnetRing


    def getParameters(self):
        """
        Retrieves the radii and magnet counts for all rings.

        Returns:
        - tuple: (numpy array of ring radii, numpy array of magnets per ring).
        """
        ringRadii = np.empty(len(self.magnetRing))
        magnetsInRingNrs = np.empty(len(self.magnetRing))

        for i in range(len(self.magnetRing)):
            ringRadii[i] = self.magnetRing[i]['ringRadius']
            magnetsInRingNrs[i] = self.magnetRing[i]['magnetsInRingNr']

        return ringRadii, magnetsInRingNrs

