from math import cos, sin, pi
import time
from direct.actor.Actor import Actor
class Ammo(Actor):
    def __init__(self,xPlayer, yPlayer,theta,time,ammonumber,id):
        Actor.__init__(self,"../model_territory/ammo2")
        self.X = xPlayer + cos(theta) * 1.5
        self.Y = yPlayer + sin(theta) * 1.5
        self.x_origine = self.X
        self.y_origine = self.Y
        self.radius = 0.5
        self.id = id
        self.time = time
        #print(self.X,self.Y,time)
        self.r = 2
        self.theta = theta
        self.number = ammonumber
        self.hit = False

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def setX(self,value):
        self.X = value

    def setY(self,value):
        self.Y = value

    def __str__(self):
        return '< AMMO id : {} | Number : {} | X : {} | Y : {} | time {}>'.format(self.id, self.number, self.X, self.Y,self.time)

    def __repr__(self):
        return '< AMMO id : {} | Number : {} | X : {} | Y : {}| time {} >'.format(self.id, self.number, self.X, self.Y,self.time)

