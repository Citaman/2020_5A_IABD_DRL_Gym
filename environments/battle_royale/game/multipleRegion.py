from direct.showbase.ShowBase import ShowBase
from direct.directbase.DirectStart import *
from panda3d.core import *
from panda3d.core import AmbientLight, DirectionalLight
from direct.gui.OnscreenImage import OnscreenImage
#from pandac.PandaModules import Texture, TextureStage, CardMaker
from direct.actor.Actor import Actor
from game.player import Player
from math import cos, sin, pi

'''
class MultipleRegion(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        cam2 = self.makeNewDr()
        cam3 = self.makeNewDr3()
        cam2.reparentTo(cam3)
        cam2.setH(15)
        self.splitScreen(cam3, cam2)

    def makeNewDr(self):
        dr2 = self.win.makeDisplayRegion(0.1, 0.4, 0.2, 0.6)
        dr2.setClearColor(VBase4(0, 0, 0, 1))
        dr2.setClearColorActive(True)
        dr2.setClearDepthActive(True)

        cam2 = self.render.attachNewNode(Camera('cam2'))
        dr2.setCamera(cam2)

        return cam2

    def makeNewDr3(self):
        dr3 = self.win.makeDisplayRegion(1, 1, 1, 1)
        dr3.setClearColor(VBase4(0, 0, 0, 1))
        dr3.setClearColorActive(True)
        dr3.setClearDepthActive(True)

        cam3 = self.render.attachNewNode(Camera('cam3'))
        dr3.setCamera(cam3)
        cam3.setPos(-22.5, -387.3, 58.1999)
        return cam3

    def splitScreen(cam, cam2):
        dr = cam.node().getDisplayRegion(0)
        dr2 = cam2.node().getDisplayRegion(0)

        dr.setDimensions(0, 0.5, 0, 1)
        dr2.setDimensions(0.5, 1, 0, 1)

        cam.node().getLens().setAspectRatio(float(dr.getPixelWidth()) / float(dr.getPixelHeight()))
        cam2.node().getLens().setAspectRatio(float(dr2.getPixelWidth()) / float(dr2.getPixelHeight()))
'''


def makeNewDr():
    dr2 = base.win.makeDisplayRegion()
    dr2.setClearColor(VBase4(0.3, 0.7, 0.5, 1))
    dr2.setClearColorActive(True)
    dr2.setClearDepthActive(True)

    cam2 = render.attachNewNode(Camera('cam2'))
    dr2.setCamera(cam2)

    return cam2


def makeNewDr3():
    dr3 = base.win.makeDisplayRegion()
    dr3.setClearColor(VBase4(0.5, 0, 0, 1))
    dr3.setClearColorActive(True)
    dr3.setClearDepthActive(True)

    cam3 = render.attachNewNode(Camera('cam3'))
    dr3.setCamera(cam3)

    return cam3

def makeNewDr4():
    dr4 = base.win.makeDisplayRegion()
    dr4.setClearColor(VBase4(1, 1, 1, 1))
    dr4.setClearColorActive(True)
    dr4.setClearDepthActive(True)

    cam4 = render.attachNewNode(Camera('cam4'))
    dr4.setCamera(cam4)

    return cam4

def makeNewDr5():
    dr5 = base.win.makeDisplayRegion()

    dr5.setClearColor(VBase4(0, 0, 0, 1))
    dr5.setClearColorActive(True)
    dr5.setClearDepthActive(True)

    cam5 = render.attachNewNode(Camera('cam5'))
    dr5.setCamera(cam5)

    return cam5


def splitScreen(cam, cam2,cam3,cam4):
    dr = cam.node().getDisplayRegion(0)
    dr2 = cam2.node().getDisplayRegion(0)
    dr3 = cam3.node().getDisplayRegion(0)
    dr4 = cam4.node().getDisplayRegion(0)


    dr.setDimensions(0, 0.5,0.5, 1) # (left, right, bottom, top)
    dr2.setDimensions(0.5, 1,0.5, 1)
    dr3.setDimensions(0, 0.5,0, 0.5)
    dr4.setDimensions(0.5, 1,0, 0.5)


    cam.node().getLens().setAspectRatio(float(dr.getPixelWidth()) / float(dr.getPixelHeight()))
    #cam2.node().getLens().setAspectRatio(float(dr2.getPixelWidth()) / float(dr2.getPixelHeight()))


cam2 = makeNewDr()
cam3 = makeNewDr3()
cam4 = makeNewDr4()
cam5 = makeNewDr5()


#cam2.reparentTo(cam3)
#cam2.setH(15)
splitScreen(cam2,cam3,cam4,cam5)

#dr = base.camNode.getDisplayRegion(0)
#dr.setActive(0)  # Or leave it (dr.setActive(1))

base.run()