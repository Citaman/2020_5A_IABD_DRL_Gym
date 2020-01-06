from math import cos, sin, pi
import time
class AmmoT():
    #vitesse d'une balle 950m/s donc 0.95 m/ miliseconde donc 0,00095 m/microseconde
    def __init__(self, xPlayer: float, yPlayer: float, theta: float, time: time, ammonumber: int, id: int, dammage: int):
        self.X = xPlayer + cos(theta) * 1.5
        self.Y = yPlayer + sin(theta) * 1.5
        self.x_origine = self.X
        self.y_origine = self.Y
        self.radius = 0.5
        self.id = id
        self.time = time
        self.dammage = dammage
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

