import random
from typing import List
import numpy as np
from collections import Counter

from math import cos, sin, pi,sqrt
from statistics import mean
from environments.battle_royale.game_Terminal.Player_terminale_mode import PlayerT
from environments.battle_royale.game_Terminal.Gun_terminal import GunT
import time

from multiprocessing import Pool
from multiprocessing import cpu_count
from functools import reduce ,partial

from contracts import GameState
from agents import RandomAgent,DeepQLearningAgent, TabQLearningAgent

class BattleRoyalGameWorldTerminal(GameState):

    def __init__(self, game_number, numberofPlayer=6, lvl=0, ratio_gun_player=1.2, list_agent=None):
        if list_agent is None:
            list_agent = [DeepQLearningAgent(action_space_size=48) if i <3 else RandomAgent() for i in range(6)]
        self.init_game_variable(game_number,numberofPlayer, lvl, ratio_gun_player, list_agent)
        self.init_game_method()

        # self.active_player = self.numberofPlayer
        self.scores = np.zeros(self.numberofPlayer)
        self.available_actions = list(range(48))
        self.unique_id = ""
        self.unique_id_vec = np.zeros(7 + (numberofPlayer - 1) * 3 + self.numberofGun * 3)

    ''' 
    def __init__(self,gameNumber):
        self.add_player()
        self.add_gun()
    '''

    def player_count(self) -> int:
        return len(self.playerwin)

    def is_game_over(self) -> bool:
        return self.win_or_not()

    def get_active_player(self) -> int:
        return 0

    def clone(self) -> 'GameState':
        pass

    def step(self, player_index: int, action_index: int):
        pass

    def get_scores(self) -> np.ndarray:
        return self.scores

    def get_available_actions(self, player_index: int) -> List[int]:
        return self.available_actions

    def __str__(self):
        pass

    def get_unique_id(self) -> str:
        return self.unique_id

    def get_max_state_count(self) -> int:
        pass

    def get_action_space_size(self) -> int:
        pass

    def get_vectorized_state(self) -> np.ndarray:
        return self.unique_id_vec

    def set_unique_id(self, player, player_X, player_Y):
        # (sqrt(pow(ammoplayer.X - player.X,2)+pow(ammoplayer.Y - player.Y,2))) <= (ammoplayer.radius + player.radius)
        # (int(el.getX()/10)+10)*21+(int(el.getY()/10)+10)
        ennemies = 0
        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if i is not player:
                    if (sqrt(pow(player_X - el.getX(), 2) + pow(player_Y - el.getY(), 2))) <= 20:
                        ennemies += 1
        gun = 0
        for (i, el) in enumerate(self.guns):
            if el.id_player == -1:
                if (sqrt(pow(player_X - el.getX(), 2) + pow(player_Y - el.getY(), 2))) <= 20:
                    gun += 1

        position = (int(player_X / 10) + 10) * 21 + (int(player_Y / 10) + 10)
        ennemies_around = 1 if ennemies > 0 else 0
        gun_around = 1 if gun > 0 else 0

        position_str = '0' * (3 - len(str(position))) + str(position)
        ennemies_around_str = str(ennemies_around)
        gun_around_str = str(gun_around)
        self.unique_id = position_str + '|' + ennemies_around_str + '|' + gun_around_str
        # print(self.unique_id)

    def set_unique_id_vec(self, id):

        self.unique_id_vec[0] = self.players[id].getX()/100
        self.unique_id_vec[1] = self.players[id].getY()/100
        self.unique_id_vec[2] = self.players[id].health/50
        self.unique_id_vec[3] = self.players[id].ammo_hit /(self.players[id].ammo_miss +1)
        self.unique_id_vec[4] = self.players[id].player_hit_me
        self.unique_id_vec[5] = self.players[id].kill
        self.unique_id_vec[6] = len(self.playerwin)

        number = 7
        for (i, el) in enumerate(self.players):
            if i is not id:
                if i not in self.playersloose and (
                sqrt(pow(self.players[id].getX() - el.getX(), 2) + pow(self.players[id].getY() - el.getY(), 2))) <= 30:
                    # print('if',number,number+1,number+2)
                    self.unique_id_vec[number] = el.getX()/100
                    self.unique_id_vec[number + 1] = el.getY()/100
                    self.unique_id_vec[number + 2] = el.health/50
                    number += 3
                else:
                    # print('else',number, number + 1, number + 2)
                    self.unique_id_vec[number] = 0
                    self.unique_id_vec[number + 1] = 0
                    self.unique_id_vec[number + 2] = 0
                    number += 3
        for (i, el) in enumerate(self.guns):
            if (sqrt(pow(self.players[id].getX() - el.getX(), 2) + pow(self.players[id].getY() - el.getY(), 2))) <= 30:
                # print('if', number, number + 1, number + 2)
                self.unique_id_vec[number] = el.getX()/100
                self.unique_id_vec[number + 1] = el.getY()/100
                self.unique_id_vec[number + 2] = el.type
                number += 3
            else:
                # print('else', number, number + 1, number + 2)
                self.unique_id_vec[number] = 0
                self.unique_id_vec[number + 1] = 0
                self.unique_id_vec[number + 2] = 0
                number += 3

        #print(self.unique_id_vec.round(2))

    def init_game_variable(self, game_number ,numberofplayer, lvl, ratio_gun_player, list_agent):
        self.state = True

        self.timeStart = time.time()
        self.earlystop = False
        self.gameNumber = game_number

        self.state_world_save = []

        self.players = []
        self.guns = []

        self.playersloose = []
        self.ratio_gun_player = ratio_gun_player
        self.numberofPlayer = numberofplayer
        self.numberofGun = int(self.numberofPlayer * self.ratio_gun_player)
        self.playerwin = [i for i in range(self.numberofPlayer)]
        self.time2 = 0
        self.frame_skip = 5
        self.count_frame = self.frame_skip
        self.frame_overall = 0
        self.level = lvl
        self.action_space_movement = 8
        self.action_space_direction = 2
        self.action_space_shoot_yes_or_not = 2
        self.list_agent = list_agent
        self.reward = []

    def init_game_method(self):
        self.add_player()
        self.add_gun()

    def add_player(self):
        r = 45
        for i in range(self.numberofPlayer):
            angleCos = cos((2*pi / self.numberofPlayer) * (i+1))
            angleSin = sin((2*pi / self.numberofPlayer) * (i+1))
            player = PlayerT(angleCos * r, angleSin * r, (i+1))
            self.players.append(player)

    def add_gun(self):
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
                                print("game world N°{} | HIT du Joueur {} sur le Jouer {} avec son tire N°{} en faisant {}".format(self.gameNumber,ammoplayer.id,player.id,ammoplayer.number,ammoplayer.dammage))
                            #print(player.id,player.health)
        #random.shuffle(self.guns)

    def play(self):

        self.death_or_not()

        self.win_or_not()
        if not self.state:
            return

        self.agent_action()

        self.gun_action()
        if self.count_frame >= self.frame_skip:
            self.count_frame = -1
            print(self.scores)
            print(self.frame_overall)

        self.count_frame += 1
        self.frame_overall += 1

    def win_or_not(self):
        if len(self.playerwin) == 1:
            winnernumber = int(self.playerwin[0])
            print("game world N°"+str(self.gameNumber)+" | "+"JOUEUR "+str(self.players[winnernumber].id) + " A GAGNE AVEC " + str(
             self.players[winnernumber].health) + " POINTS DE VIE" + " ET avec un ratio de "+str(
             round((self.players[winnernumber].ammo_hit/self.players[winnernumber].ammonumber),4)*100)+"%  | Nombre de Hit : "+str(self.players[winnernumber].ammo_hit)+" Nombre de Shoot : "+str(self.players[winnernumber].ammonumber)+" | Gun "+str( self.players[winnernumber].gun.name if self.players[winnernumber].has_a_gun else None))
            self.state = False

        if len(self.playerwin) == 0:
            # print("game world N°" + str(self.gameNumber) + " | NO WINNER ")
            self.state = False

    def death_or_not(self):
        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if el.get_health() <= 0:
                    if self.players[i].has_a_gun:
                        self.players[i].gun.get_release()
                    self.players[i].erase_ammo()
                    self.playersloose.append(i)
                    self.playerwin.remove(i)
                    print("game world N°"+str(self.gameNumber)+" | "+"Player " + str(i) + " est mort")

    def gun_action(self):
        for (i, gun) in enumerate(self.guns):
            for (j, player) in enumerate(self.players):
                if j not in self.playersloose:
                    if gun.id_player == -1:
                        if not player.has_a_gun or time.time() - player.time_pick >= player.time_delay_pick:
                            if (sqrt(pow(gun.X - player.X, 2) + pow(gun.Y - player.Y, 2))) <= (
                                    gun.radius + player.radius):
                                if player.has_a_gun:
                                    self.players[j].gun.get_release()
                                    print("RELEASE {} {}     Release By   {} in World {} ".format(self.players[j].gun.name,self.players[j].gun.id_gun,player.id,self.gameNumber))
                                self.players[j].gun = gun
                                self.players[j].has_a_gun = True
                                self.players[j].time_pick = time.time()
                                self.guns[i].get_pickup(player.id, player.getX(), player.getY(), 5,
                                                        player.shoot_decision)
                                print("PICK {}  {}    Pick By   {} in World {} ".format(gun.name, gun.id_gun, player.id,self.gameNumber))

    def agent_action(self):
        old_scores = self.scores.copy()
        action_per_agent=[]
        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if self.count_frame >= self.frame_skip:
                    '''AGENT ACTION'''
                    self.set_unique_id(i, el.getX(), el.getY())
                    self.set_unique_id_vec(i)
                    action = self.list_agent[i].act(gs=self)
                    action_per_agent.append(action)
                    '''try:
                        print(self.list_agent[i].Q)
                    except:
                        pass'''

                    shoot_or_not = 1 if action >= 24 else 0
                    action_second = action - 24 if action >= 24 else action

                    random_cut = action_second % 8
                    power_move = int(action_second / 8)
                    el.shoot_or_not_decision = shoot_or_not

                    #print("action",action,"shoot or not", shoot_or_not, "direction",random_cut,"speed",power_move)

                    theta_move = (2 * pi / (self.action_space_movement)) * (random_cut)  # random.uniform(0,2*pi)
                    # print( "random cut",random_cut,"power", power_move)
                    if self.level > 0:
                        random_cut2 = random.choice(list(range(17)))
                        thetashoot = (2 * pi / (16)) * (random_cut2)
                    else:
                        thetashoot = theta_move

                    el.X_decision = cos(theta_move) * power_move / 2
                    el.Y_decision = sin(theta_move) * power_move / 2

                el.move()
                el.attack(time=time.time())
                el.ammoshoot(time=time.time())
                position = (int(el.getX() / 10) + 10) * 21 + (int(el.getY() / 10) + 10)
                position_str = '0' * (3 - len(str(position))) + str(position)
                if position_str not in el.discovery:
                    el.discovery.append(position_str)
                self.scores[i] = el.kill*0.5+ el.ammo_hit * 0.2 + len(el.discovery) *0.1 + (el.health-50)*0.1 - el.ammo_miss * 0.1


            new_scores = self.scores
            rewards = new_scores - old_scores
            self.reward = rewards.copy()
            # print(new_scores,old_scores)
            for i, agent in enumerate(self.list_agent):
                agent.observe(rewards[i], self.is_game_over(), i)


        if self.count_frame >= self.frame_skip:
            print(action_per_agent)

    def run(self):
        # tic = time.time()
        # maxTime = 0.8
        max_frame = 550#5500
        while(self.state):
            self.play()
            self.colision()
            if self.frame_overall - max_frame >= 0: # time.time() - tic  >= maxTime:
                self.state = False
                self.earlystop = True
        # print(self.frame_overall)
        if not self.earlystop :
            for i, agent in enumerate(self.list_agent):
                agent.observe(self.reward[i],True,i)
            #print("dnfodfojqdkslm,fndvbjfklpionqdklsoifqmjkd ln,opIJFGODKL,sijfomgjk")
            # toc = time.time()
            # print("game world N°"+str(self.gameNumber)+" | "+"GAME FINISH IN : "+str(round(toc-tic,4))+" secondes")
            # return float(toc-tic)
            # return 1
            return self.frame_overall,len(self.playerwin)
        else :
            for i, agent in enumerate(self.list_agent):
                agent.observe(self.reward[i], True, i)
            #print("dnfodfojqdkslm,fndvbjfklpionqdklsoifqmjkd ln,opIJFGODKL,sijfomgjk")
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
    list_agent = [DeepQLearningAgent(action_space_size=48) if i < 3 else TabQLearningAgent() for i in range(6)]
    Terminalworld = BattleRoyalGameWorldTerminal(i,list_agent=list_agent)
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
        #func = partial(run_BattleRoyal, list_agent)
        result = p.map_async(run_BattleRoyal,range(2))
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
    
    
    #print(mean(avgtime) , sum(avgtime))