from direct.actor.Actor import Actor
from math import cos, sin, pi, sqrt, pow

from panda3d.core import CollisionNode, CollisionSphere
import warnings

warnings.filterwarnings("ignore")

import random


class Gun(Actor):
    def __init__(self, X, Y, Z, id, type):

        self.seconde_between_shoot = 0
        self.distance_of_shoot = 0
        self.min_damage = 0
        self.max_damage = 0
        self.id_gun = id
        self.id_player = -1
        self.type = 0
        self.collider = None

        if type == 1:
            Actor.__init__(self, "model_territory/AK-47")
            self.setPos(X, Y, Z)
            self.setHpr(0, 90, 0)
            self.type = 1
            self.seconde_between_shoot = 0.15
            self.distance_of_shoot = 30
            self.min_damage = 10
            self.max_damage = 17
            self.setScale(0.8)
            self.collider = self.attach_new_node(CollisionNode('Gun/'+'AK-47'+"/"+str(self.id_gun)))
            self.collider.node().addSolid(CollisionSphere(0, 0, 0, 5))
            self.collider.show()


        elif type == 2:
            Actor.__init__(self, "model_territory/Fusil_a_pompe")
            self.setPos(X, Y, Z)
            self.setHpr(0, 90, 0)
            self.type = 2
            self.seconde_between_shoot = 0.8
            self.distance_of_shoot = 10
            self.min_damage = 25
            self.max_damage = 40
            self.collider = self.attach_new_node(CollisionNode('Gun/'+'Fusil_a_pompe'+"/"+str(self.id_gun)))
            self.collider.node().addSolid(CollisionSphere(0, 0, 0, 1))
            self.collider.show()
            self.setScale(4)

        elif type == 3:
            Actor.__init__(self, "model_territory/ColtPython")
            self.setPos(X, Y, Z)
            self.setHpr(0, 90, 0)
            self.type = 3
            self.seconde_between_shoot = 0.4
            self.distance_of_shoot = 20
            self.min_damage = 8
            self.max_damage = 14
            self.collider = self.attach_new_node(CollisionNode('Gun/'+'ColtPython'+"/"+str(self.id_gun)))
            self.collider.node().addSolid(CollisionSphere(0, 0, 0, 1))
            self.collider.show()
            self.setScale(2)

        else:
            self.type = 4
            self.seconde_between_shoot = 0.4
            self.distance_of_shoot = 20
            self.min_degat = 8
            self.max_degat = 14

    def get_pickup(self,id_player,X,Y,Z,theta):
        self.id_player = id_player
        self.setPos((X + cos(theta)*3.5,Y + sin(theta)*3.5, 2))
        self.setHpr(0, 0, 0)
        self.collider.node().clearSolids()

    def get_release(self):
        self.id_player = -1
        self.collider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        theta = random.uniform(0,2*pi)
        r = 10
        self.setPos(self.getPos()+(cos(theta)*r,sin(theta)*r, 2))
        self.setHpr(0, 90, 0)

    def move(self,pos,theta):
        self.setPos(pos + (cos(theta)*3.5,sin(theta)*3.5,0))  # *(180/pi)
        self.setHpr(theta*(180/pi), 0, 0)










