class HsvFilter:

    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None, sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.hMax = hMax
        self.vMin = vMin
        self.vMax = vMax
        self.sMin = sMin
        self.sMax = sMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub