from direct.actor.Actor import Actor
from math import cos, sin, pi, sqrt,pow

from panda3d.core import CollisionNode,CollisionSphere
import warnings
warnings.filterwarnings("ignore")
import sys
import random

class Player(Actor):
    def __init__(self,X,Y,Z,id):
        #sys.path.append('/Users/anthonnyolime/Git-Projet/2020_5A_IABD_DRL_Gym/environments/battle_royale/game')
        Actor.__init__(self,"model_territory/Android")
        self.setPos(X, Y, Z)
        self.X_decision = 0
        self.Y_decision = 0
        self.shoot_decision = 0
        self.shoot_or_not_decision = 0
        self.setScale(2)
        self.text = None
        self.textstr = None
        self.max_distance = 50
        #print(self.getTightBounds())
        self.shoot=[]
        self.shootTimeDelay = 0.5
        # AK-45 : 0.15 | 30
        # coltPython : 0.4 | 20
        # fusil_a_pompe : 0.8 | 10
        # main nue : 0.5 | 3
        self.time_delay_pick = 10
        self.time_pick = 0
        self.guntype = 0
        self.has_a_gun = False
        self.gun = None

        self.player_hit_me = -1
        self.shootTimeDelayNow = 0
        self.id = id
        # self.health = 50
        self.health = 25
        self.ammonumber = 0
        self.ammo_hit = 0
        self.ammo_miss = 0
        self.kill = 0

        self.score = 0

        self.discovery = []

    # r le radius
    # theta en degré ( 1 radian * 180/pi = 57,3 °) et ( 1° * pi/180 = 0.017 rad)
    def attack(self,render,time):
        if time - self.shootTimeDelayNow >= (self.shootTimeDelay if not self.has_a_gun else self.gun.seconde_between_shoot)  and self.shoot_or_not_decision>0.5 :
            theta = self.shoot_decision
            shootammo = Actor("model_territory/ammo2")
            shootammo.reparentTo(render)
            shootammo.setPos(self.getPos()+(cos(theta)*1.5,sin(theta)*1.5,5))
            #print(shootammo.getPos())
            shootammo.setScale(4)
            shootammo.setColor(1,0.,0,1.0)

            if not self.has_a_gun :
                shootammo.dammage = random.randint(2,8)
            else:
                shootammo.dammage = random.randint(self.gun.min_damage, self.gun.max_damage)

            shootammo.id = self.id
            shootammo.x_origine = shootammo.getX()
            shootammo.y_origine = shootammo.getY()
            shootammo.time = time
            shootammo.r = 4
            shootammo.theta = theta
            shootammo.number = self.ammonumber
            shootammo.hit = False
            a =shootammo.attach_new_node(CollisionNode('ammo/' + str(self.id)+'/'+str(self.ammonumber)))
            a.node().addSolid(CollisionSphere(0, 0, 0, 0.5))
            a.show()
            #print(shootammo.getTightBounds())



            self.shoot.append(shootammo)
            self.shootTimeDelayNow = time
            self.ammonumber += 1

    def ammoshoot(self,time):
        copy_list = self.shoot
        for (i, el) in enumerate(copy_list):
            if el.hit:
                self.shoot[i].delete()
                self.shoot.pop(i)
                self.ammo_hit += 1
            elif (sqrt(pow(el.x_origine - el.getX(),2)+pow(el.y_origine - el.getY(),2))) >=(self.gun.distance_of_shoot if self.has_a_gun else 3):
                self.shoot[i].delete()
                self.shoot.pop(i)
                self.ammo_miss += 1
            elif self.shoot[i].getX() > self.max_distance or self.shoot[i].getX() < -self.max_distance or self.shoot[i].getY() < -self.max_distance or self.shoot[
                i].getY() > self.max_distance:
                self.shoot[i].delete()
                self.shoot.pop(i)
                self.ammo_miss += 1
            else:
                angleCos = cos(el.theta)
                angleSin = sin(el.theta)
                self.shoot[i].setX(self.shoot[i].getX() + angleCos * el.r)
                self.shoot[i].setY(self.shoot[i].getY() + angleSin * el.r)
                #print(self.shoot[i].getPos())

    def move(self):
        self.textstr.set_text(
            str(self.id) + " " + str(self.health) + "PV" + " " + str(round(self.score,3)) + " points")
        if self.getY() + self.Y_decision > self.max_distance:
            self.setY(self.max_distance)
            self.text.setY(self.max_distance)
        elif self.getY() + self.Y_decision < -self.max_distance:
            self.setY(-self.max_distance)
            self.text.setY(-self.max_distance)
        else:
            self.setY(self.getY() + self.Y_decision)
            self.text.setY(self.text.getY() + self.Y_decision)

        if self.getX() + self.X_decision > self.max_distance:
            self.setX(self.max_distance)
            self.text.setX(self.max_distance-25)
        elif self.getX() + self.X_decision < -self.max_distance:
            self.setX(-self.max_distance)
            self.text.setX(-self.max_distance-25)
        else:
            self.setX(self.getX() + self.X_decision)
            self.text.setX(self.text.getX() + self.X_decision)

    def get_health(self):
        return self.health

    def erase_ammo(self):
        copy_list = self.shoot
        for (i,el) in enumerate(copy_list):
            self.shoot[i].delete()

    def __str__(self):
        return 'PLAYER< id : {} | PV : {} | X : {} | Y : {} >'.format(self.id, self.health, self.getX(), self.getY())
