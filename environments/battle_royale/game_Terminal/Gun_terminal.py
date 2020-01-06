from math import cos, sin, pi
import random


class GunT():
    def __init__(self, X, Y, Z, id, type):

        self.seconde_between_shoot = 0
        self.distance_of_shoot = 0
        self.min_damage = 0
        self.max_damage = 0
        self.id_gun = id
        self.id_player = -1
        self.type = 0
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.radius = 1.5
        self.name = 'None'

        if type == 1:
            self.type = 1
            self.name = 'AK-47'
            self.seconde_between_shoot = 0.00015
            self.distance_of_shoot = 30
            self.min_damage = 10
            self.max_damage = 17


        elif type == 2:
            self.type = 2
            self.name = 'Fusil_a_pompe'
            self.seconde_between_shoot = 0.0008
            self.distance_of_shoot = 10
            self.min_damage = 25
            self.max_damage = 40

        elif type == 3:
            self.type = 3
            self.name = 'ColtPython'
            self.seconde_between_shoot = 0.0004
            self.distance_of_shoot = 20
            self.min_damage = 8
            self.max_damage = 14
            self.radius = 1

        else:
            self.type = 4
            self.seconde_between_shoot = 0.4
            self.distance_of_shoot = 20
            self.min_degat = 8
            self.max_degat = 14

    def get_pickup(self,id_player,X,Y,Z,theta):
        self.id_player = id_player
        self.setPos((X + cos(theta)*3.5,Y + sin(theta)*3.5, 2))

    def get_release(self):
        self.id_player = -1
        theta = random.uniform(0,2*pi)
        r = 10
        self.setPos(self.getPos()+(cos(theta)*r,sin(theta)*r, 2))

    def getPos(self):
        return (self.X,self.Y,self.Z)

    def setPos(self,tuple):
        self.X= tuple[0]
        self.Y = tuple[1]
        self.Z = tuple[2]

    #def move(self,pos,theta):
        #self.setPos(pos + (cos(theta)*3.5,sin(theta)*3.5,0))  # *(180/pi)

    def __str__(self):
        return 'Gun <  Name : {}  |id_gun : {} |id_player : {} | X : {} | Y : {} >'.format(self.name,self.id_gun,self.id_player,self.X, self.Y)

    def __repr__(self):
        return 'Gun <  Name : {}  |id_gun: {} |id_player : {} | X : {} | Y : {} >'.format(self.name,self.id_gun,self.id_player,self.X, self.Y)










