from math import cos, sin, pi,sqrt
from .Ammo_terminale import AmmoT
from time import sleep
import random
import time as time2
class PlayerT:
    def __init__(self,X,Y,id):
        self.X = X
        self.Y = Y
        self.radius = 2
        self.shoot=[]
        self.X_decision = 0
        self.Y_decision = 0
        self.shoot_decision = 0
        self.shoot_or_not_decision = 0
        self.max_distance = 50
        self.reward = 0

        self.shootTimeDelay = 0.0005
        self.shootTimeDelayNow = 0

        self.time_delay_pick = 0.01
        self.time_pick = 0
        self.guntype = 0
        self.has_a_gun = False
        self.gun = None

        self.timeshootsave = time2.time()
        self.id = id
        self.health = 50
        self.ammonumber = 0
        self.ammo_hit = 0
        self.ammo_miss = 0
        self.kill = 0
        self.player_hit_me = -1
        self.discovery = []

    # r le radius
    # theta en degré ( 1 radian * 180/pi = 57,3 °) et ( 1° * pi/180 = 0.017 rad)
    def attack(self,time):
        #print(self.shootTimeDelayNow, (self.shootTimeDelay if not self.has_a_gun else self.gun.seconde_between_shoot) ,self.shoot_or_not_decision, self.shoot_or_not_decision>0.5)
        if time - self.shootTimeDelayNow >= (self.shootTimeDelay if not self.has_a_gun else self.gun.seconde_between_shoot) and self.shoot_or_not_decision>0.5:
            theta = self.shoot_decision
            dammage = random.randint(2,8) if not self.has_a_gun else random.randint(self.gun.min_damage, self.gun.max_damage)
            shootammo = AmmoT(self.X,self.Y,self.shoot_decision,time,self.ammonumber,self.id,dammage)
            shootammo.r = 4
            shootammo.theta = theta
            self.shoot.append(shootammo)
            self.shootTimeDelayNow = time
            self.ammonumber += 1

    def ammoshoot(self,time):
        copy_list = self.shoot
        for (i, el) in enumerate(copy_list):
            if el.hit:
                self.shoot.pop(i)
                self.ammo_hit += 1
            # elif time - el.time >= 0.001:
                # self.shoot.pop(i)
            elif (sqrt(pow(el.x_origine - el.getX(),2)+pow(el.y_origine - el.getY(),2))) >= (self.gun.distance_of_shoot if self.has_a_gun else 3):
                self.shoot.pop(i)
                self.ammo_miss +=1
            elif self.shoot[i].getX() >= self.max_distance or self.shoot[i].getX() <= -self.max_distance or self.shoot[i].getY() <= -self.max_distance or self.shoot[i].getY() >= self.max_distance:
                self.shoot.pop(i)
                self.ammo_miss += 1
            else:
                angleCos = cos(el.theta)
                angleSin = sin(el.theta)
                #print("Ammo" ,self.id,el.number ,(sqrt(pow(el.x_origine - el.getX(),2)+pow(el.y_origine - el.getY(),2))))
                #print( angleCos * el.r, angleSin * el.r)
                self.shoot[i].setX(self.shoot[i].getX() + angleCos * el.r)
                self.shoot[i].setY(self.shoot[i].getY() + angleSin * el.r)

            #print(time - self.timeshootsave)
            #self.timeshootsave = time
                #sleep(1)


    def get_health(self):
        return self.health

    def erase_ammo(self):
        self.shoot.clear()

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def setX(self,value):
        self.X = value

    def setY(self,value):
        self.Y = value

    def move(self):
        if self.getY() + self.Y_decision > self.max_distance:
            self.setY(self.max_distance)
        elif self.getY() + self.Y_decision < -self.max_distance:
            self.setY(-self.max_distance)
        else:
            self.setY(self.getY() + self.Y_decision)

        if self.getX() + self.X_decision > self.max_distance:
            self.setX(self.max_distance)
        elif self.getX() + self.X_decision < -self.max_distance:
            self.setX(-self.max_distance)
        else:
            self.setX(self.getX() + self.X_decision)

    def __str__(self):
        if self.has_a_gun:
            return 'PLAYER< id : {} | PV : {} | X : {} | Y : {} | Gun {} | Nombre Hit {} >'.format(self.id, self.health,
                                                                                                   self.X, self.Y,
                                                                                                   self.gun.name,
                                                                                                   self.ammonumber)
        else:
            return 'PLAYER< id : {} | PV : {} | X : {} | Y : {} | Gun {} | Nombre Hit {} >'.format(self.id, self.health,
                                                                                                   self.X, self.Y,
                                                                                                   None,
                                                                                                   self.ammonumber)

    def __repr__(self):
        if self.has_a_gun:
            return 'PLAYER< id : {} | PV : {} | X : {} | Y : {} | Gun {} | Nombre Hit {} >'.format(self.id, self.health, self.X, self.Y,self.gun.name,self.ammonumber)
        else:
            return 'PLAYER< id : {} | PV : {} | X : {} | Y : {} | Gun {} | Nombre Hit {} >'.format(self.id, self.health,
                                                                                                   self.X, self.Y,
                                                                                                   None,
                                                                                                   self.ammonumber)


