import random
import time
import sys
import numpy as np
#sys.path.append('/path/to/game_Terminal')
#sys.path.append('/Users/anthonnyolime/PycharmProjects/BATTLE_ROYALE')
from collections import Counter
#print(sys.path)
from math import cos, sin, pi,sqrt
from statistics import mean
from environments.battle_royale.game_Terminal.Player_terminale_mode import PlayerT
from environments.battle_royale.game_Terminal.Gun_terminal import GunT
import time
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import cpu_count
from functools import reduce



class BattleRoyalGameWorldTerminal():
    def __init__(self,gameNumber):

        self.state = True
        self.players = []
        self.guns = []
        self.playersloose = []
        self.numberofPlayer = 6
        self.numberofGun = 8
        self.playerwin = [i for i in range(self.numberofPlayer)]
        self.timeStart = time.time()
        self.earlystop = False
        self.gameNumber = gameNumber
        self.frame_skip = 20
        self.count_frame = 20
        self.frame_overall = 0

        self.state_world_save = []
        self.addPlayer()
        self.addGun()

    def addPlayer(self):
        r = 45
        for i in range(self.numberofPlayer):
            angleCos = cos((2*pi / self.numberofPlayer) * (i+1))
            angleSin = sin((2*pi / self.numberofPlayer) * (i+1))
            player = PlayerT(angleCos * r, angleSin * r, (i+1))
            self.players.append(player)

    def addGun(self):
        # r = 50
        type_gun = np.array([1,2,3])
        probabilities_apparition = np.array([0, 0.2, 0.8])
        distribution_gun = np.random.choice(type_gun, self.numberofGun, p=probabilities_apparition)
        for (i, el) in enumerate(distribution_gun):
            angleCos = cos((2 * pi / self.numberofGun) * (i + 1)+random.uniform(-0.5, 0.5))
            angleSin = sin((2 * pi / self.numberofGun) * (i + 1)+random.uniform(-0.5, 0.5))
            r = random.uniform(20,35)
            gun = GunT(angleCos * r, angleSin * r, 2, i, el)
            # gun.reparentTo(self.render)
            self.guns.append(gun)

    def colision(self):
        ammo = [player.shoot for player in self.players]
        ammo2 = reduce(lambda x,y:x+y,ammo)
        #print(len(ammo2))
        #random.shuffle(ammo2)
        for ammoplayer in ammo2:
            for (i, player) in enumerate(self.players):
                if i not in self.playersloose:
                    if ammoplayer.id != player.id :
                        #print(sqrt(pow(ammoplayer.X - player.X,2)+pow(ammoplayer.Y - player.Y,2)))
                            if (sqrt(pow(ammoplayer.X - player.X,2)+pow(ammoplayer.Y - player.Y,2))) <= (ammoplayer.radius + player.radius) and not ammoplayer.hit:
                                ammoplayer.hit = True
                                player.health -= ammoplayer.dammage
                                #print("game world N°{} | HIT du Joueur {} sur le Jouer {} avec son tire N°{} en faisant {}".format(self.gameNumber,ammoplayer.id,player.id,ammoplayer.number,ammoplayer.dammage))
                            #print(player.id,player.health)
        #random.shuffle(self.guns)

    def play(self):

        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if el.get_health() <= 0:
                    if self.players[i].has_a_gun : self.players[i].gun.get_release()
                    self.players[i].erase_ammo()
                    self.playersloose.append(i)
                    self.playerwin.remove(i)
                    #print("game world N°"+str(self.gameNumber)+" | "+"Player " + str(i) + " est mort")

        if len(self.playerwin) == 1:
            winnernumber = int(self.playerwin[0])
            #print("game world N°"+str(self.gameNumber)+" | "+"JOUEUR "+str(self.players[winnernumber].id) + " A GAGNE AVEC " + str(
                #self.players[winnernumber].health) + " POINTS DE VIE" + " ET avec un ratio de "+str(
                #round((self.players[winnernumber].ammohit/self.players[winnernumber].ammonumber),4)*100)+"%  | Nombre de Hit : "+str(self.players[winnernumber].ammohit)+" Nombre de Shoot : "+str(self.players[winnernumber].ammonumber)+" | Gun "+str( self.players[winnernumber].gun.name if self.players[winnernumber].has_a_gun else None))
            self.state=False
            return
        if len(self.playerwin) == 0:
            #print("game world N°" + str(self.gameNumber) + " | NO WINNER ")
            self.state = False
            return

        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if self.count_frame >= self.frame_skip:
                    random_cut = random.choice(list(range(17)))
                    thetamove = (2 * pi / (16)) * (random_cut)  # random.uniform(0,2*pi)
                    rmove = random.choice(list(range(17)))
                    el.X_decision = cos(thetamove) * rmove / 24 if rmove >= 4 else 0
                    el.Y_decision = sin(thetamove) * rmove / 24 if rmove >= 4 else 0

                    random_cut2 = random.choice(list(range(17)))
                    thetashoot = (2 * pi / (16)) * (random_cut2)
                    el.shoot_decision = thetashoot
                    el.shoot_or_not_decision = random.random()

                el.move()
                el.attack(time=time.time())
                el.ammoshoot(time=time.time())

        if self.count_frame >= self.frame_skip:
            self.count_frame = -1

        self.count_frame += 1
        self.frame_overall += 1

        for (i, gun) in enumerate(self.guns):
            for (j, player) in enumerate(self.players):
                if j not in self.playersloose:
                    if gun.id_player == -1:
                        if not player.has_a_gun or time.time() - player.time_pick >=player.time_delay_pick :
                            if (sqrt(pow(gun.X - player.X, 2) + pow(gun.Y - player.Y, 2))) <= (
                                    gun.radius + player.radius):
                                if player.has_a_gun:
                                    self.players[j].gun.get_release()
                                    #print("RELEASE {} {}     Release By   {} in World {} ".format(self.players[j].gun.name,self.players[j].gun.id_gun,player.id,self.gameNumber))
                                self.players[j].gun = gun
                                self.players[j].has_a_gun = True
                                self.players[j].time_pick = time.time()
                                self.guns[i].get_pickup(player.id, player.getX(), player.getY(), 5,
                                                        player.shoot_decision)
                                #print("PICK {}  {}    Pick By   {} in World {} ".format(gun.name, gun.id_gun, player.id,self.gameNumber))

    def run(self):
        # tic = time.time()
        # maxTime = 0.8
        max_frame = 5500
        while(self.state):
            self.play()
            self.colision()
            if self.frame_overall - max_frame >= 0: # time.time() - tic  >= maxTime:
                self.state = False
                self.earlystop = True
        # print(self.frame_overall)
        if not self.earlystop :
            # toc = time.time()
            # print("game world N°"+str(self.gameNumber)+" | "+"GAME FINISH IN : "+str(round(toc-tic,4))+" secondes")
            # return float(toc-tic)
            # return 1
            return self.frame_overall,len(self.playerwin)
        else :
            # print("game world N°" + str(self.gameNumber) + " | " + "Early Stoping | Stile : "+str(self.playerwin))
            # for player in self.players :print(player)
            # return float(maxTime)
            # return len(self.playerwin)
            return max_frame,len(self.playerwin)

    def save_state(self):
        pass

    def givereward(self):
        pass



def run_BattleRoyal(i):
    Terminalworld = BattleRoyalGameWorldTerminal(i)
    a = Terminalworld.run()
    return a

# Terminalworld = BattleRoyalGameWorldTerminal(1)
# Terminalworld.run()


'''
tic = time.time()
for i in range(10):
    result_frame =[]
    result_winnerPlace =[]
    for j in range(100):
        res = run_BattleRoyal(i)
        result_frame.append(res[0])
        result_winnerPlace.append(res[1])
    print(Counter(result_frame))
    print(Counter(result_winnerPlace))

print("Without Multiprocessing", tic - time.time())
'''
'''
tic = time.time()
#print(multiprocessing.cpu_count())
for i in range(12):
    Terminalworld = BattleRoyalGameWorldTerminal(i)
    p1 = Process(target=Terminalworld.run, name= 'gameWrold-{}'.format(i))
    p1.start()
    #p1.join()

toc = time.time()
print("PROCESS METHOD"+" | "+"ALL GAMES FINISH IN : "+str(round(toc-tic))+" secondes")
'''
if __name__ == '__main__':
    avgtime = []
    for i in range(10):
        p = Pool(cpu_count())
        print(cpu_count())
        result = p.map_async(run_BattleRoyal,range(100))
        tic = time.time()
        p.close()
        p.join()
        toc = time.time()
        avgtime.append(toc-tic)
        print("POOL METHOD"+" | "+"ALL GAMES FINISH IN : "+str(round(toc-tic,4))+" secondes")
        #print(Counter((result.get())))
        result_frame = reduce(lambda acc, x: acc + (x[0],), result.get(), ())
        result_winnerPlace = reduce(lambda acc, x: acc + (x[1],), result.get(), ())
        #print(result.get())
        print(Counter(result_frame))
        print(Counter(result_winnerPlace))
        time.sleep(1)

    print(mean(avgtime) , sum(avgtime))