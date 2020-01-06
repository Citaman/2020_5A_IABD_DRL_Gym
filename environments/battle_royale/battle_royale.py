from typing import List

import sys

import random
from math import cos, sin, pi,sqrt
import numpy as np

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

from agents import RandomAgent
from contracts import GameState
from environments.battle_royale.game import Player, Gun


class BattleRoyale(GameState, ShowBase):
    def __init__(self,numberofPlayer = 6,lvl =0,ratio_gun_player=0.8,list_agent=[RandomAgent() for _ in range(6)]):
        ShowBase.__init__(self)
        self.init_game_variable(numberofPlayer,lvl,ratio_gun_player,list_agent)
        self.init_game_method()
        self.init_taskMgr()

        # self.active_player = self.numberofPlayer
        self.scores = np.zeros(self.numberofPlayer)
        self.available_actions = list(range(48))
        self.unique_id = ""
        self.unique_id_vec = np.zeros(7+(numberofPlayer-1)*3+self.numberofGun*3)


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

    def set_unique_id(self,player,player_X,player_Y):
        # (sqrt(pow(ammoplayer.X - player.X,2)+pow(ammoplayer.Y - player.Y,2))) <= (ammoplayer.radius + player.radius)
        # (int(el.getX()/10)+10)*21+(int(el.getY()/10)+10)
        ennemies =0
        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if i is not player:
                    if (sqrt(pow(player_X - el.getX(),2)+pow(player_Y - el.getY(),2))) <= 20 :
                        ennemies +=1
        gun = 0
        for (i, el) in enumerate(self.guns):
            if el.id_player == -1 :
                if (sqrt(pow(player_X - el.getX(), 2) + pow(player_Y - el.getY(), 2))) <= 20:
                    gun +=1

        position = (int(player_X/10)+10)*21+(int(player_Y/10)+10)
        ennemies_around = 1 if ennemies >0 else 0
        gun_around = 1 if gun >0 else 0

        position_str =  '0' * (3 - len(str(position))) + str(position)
        ennemies_around_str = str(ennemies_around)
        gun_around_str = str(gun_around)
        self.unique_id = position_str+'|'+ennemies_around_str+'|'+gun_around_str
        #print(self.unique_id)

    def set_unique_id_vec(self,id):

        self.unique_id_vec[0]= self.players[id].getX()
        self.unique_id_vec[1] = self.players[id].getY()
        self.unique_id_vec[2] = self.players[id].health
        self.unique_id_vec[3] = self.players[id].ammo_hit
        self.unique_id_vec[4] = self.players[id].ammo_miss
        self.unique_id_vec[5] = self.players[id].kill
        self.unique_id_vec[6] = len(self.playerwin)

        number = 7
        for (i, el) in enumerate(self.players):
            if i is not id:
                if i not in self.playersloose and (sqrt(pow(self.players[id].getX() - el.getX(),2)+pow(self.players[id].getY()- el.getY(),2))) <= 30 :
                    #print('if',number,number+1,number+2)
                    self.unique_id_vec[number] = el.getX()
                    self.unique_id_vec[number+1] = el.getY()
                    self.unique_id_vec[number + 2] = el.health
                    number += 3
                else:
                    #print('else',number, number + 1, number + 2)
                    self.unique_id_vec[number] = 0
                    self.unique_id_vec[number + 1] = 0
                    self.unique_id_vec[number + 2] = 0
                    number += 3
        for (i, el) in enumerate(self.guns):
                if (sqrt(pow(self.players[id].getX() - el.getX(), 2) + pow(self.players[id].getY() - el.getY(), 2))) <= 30:
                    #print('if', number, number + 1, number + 2)
                    self.unique_id_vec[number] = el.getX()
                    self.unique_id_vec[number + 1] = el.getY()
                    self.unique_id_vec[number + 2] = el.type
                    number += 3
                else:
                    #print('else', number, number + 1, number + 2)
                    self.unique_id_vec[number] = 0
                    self.unique_id_vec[number + 1] = 0
                    self.unique_id_vec[number + 2] = 0
                    number += 3


        print(self.unique_id_vec)

    def get_max_state_count(self) -> int:
        pass

    def get_action_space_size(self) -> int:
        return 48

    def get_vectorized_state(self) -> np.ndarray:
        return self.unique_id_vec

    '''GAME ENGINE  BELOW'''

    def init_game_variable(self,numberofplayer,lvl,ratio_gun_player,list_agent):
        self.keyMap = {"left": False, "right": False, "forward": False, "backward": False, "shoot": False}
        self.players = []
        self.guns = []
        self.traverser = CollisionTraverser('traverser name')
        self.queue = CollisionHandlerQueue()
        self.playersloose = []
        self.ratio_gun_player = ratio_gun_player
        self.numberofPlayer = numberofplayer
        self.numberofGun = int(self.numberofPlayer*self.ratio_gun_player)
        print("Number of player",self.numberofPlayer,"Number of gun",self.numberofGun)
        self.playerwin = [i for i in range(self.numberofPlayer)]
        self.time2 = 0
        self.frame_skip = 5
        self.count_frame = self.frame_skip
        self.level = lvl
        self.action_space_movement = 8
        self.action_space_direction = 2
        self.action_space_shoot_yes_or_not = 2
        self.list_agent = list_agent

    def init_taskMgr(self):
        self.taskMgr.add(self.move_camera, "move the camera")
        self.taskMgr.add(self.collision, "collision")
        self.taskMgr.add(self.play, "play")

    def init_game_method(self):
        self.action()
        self.add_terrain()
        self.add_light()
        self.background_image("clear-blue-sky.jpeg")
        self.add_player()
        self.add_gun()
        self.disableMouse()
        self.camera_set()

    def action(self):
        self.accept("arrow_left", self.set_key, ["left", True])
        self.accept("arrow_right", self.set_key, ["right", True])
        self.accept("arrow_up", self.set_key, ["forward", True])
        self.accept("arrow_down", self.set_key, ["backward", True])
        self.accept("arrow_left-up", self.set_key, ["left", False])
        self.accept("arrow_right-up", self.set_key, ["right", False])
        self.accept("arrow_up-up", self.set_key, ["forward", False])
        self.accept("arrow_down-up", self.set_key, ["backward", False])
        self.accept("space", self.set_key, ["shoot", True])
        self.accept("space-up", self.set_key, ["shoot", False])

    def set_key(self, key, value):
        self.keyMap[key] = value

    def add_player(self):
        r = 80
        for i in range(self.numberofPlayer):
            angleCos = cos((2 * pi / (self.numberofPlayer)) * (i + 1))
            angleSin = sin((2 * pi / (self.numberofPlayer)) * (i + 1))
            player = Player(angleCos * r, angleSin * r, 0, i)
            player.reparentTo(self.render)
            playerColision = player.attach_new_node(CollisionNode('player/' + str(i) + "/0"))
            playerColision.node().addSolid(CollisionCapsule(ax=0, ay=0, az=4, bx=0, by=0, bz=0, radius=1.1))
            # player.node().removeSolid()
            # playerColision.show()
            self.traverser.addCollider(playerColision, self.queue)
            self.players.append(player)

            #add Agent
            self.list_agent[i].playerid = i

    def add_gun(self):
        # r = 50
        type_gun = np.array([1, 2, 3])
        probabilities_apparition = np.array([0.1, 0.8, 0.1])
        distribution_gun = np.random.choice(type_gun, self.numberofGun, p=probabilities_apparition)
        for (i, el) in enumerate(distribution_gun):
            angleCos = cos((2 * pi / (self.numberofGun)) * (i + 1) + random.uniform(-0.5, 0.5))
            angleSin = sin((2 * pi / (self.numberofGun)) * (i + 1) + random.uniform(-0.5, 0.5))
            r = random.uniform(45, 65)
            gun = Gun(angleCos * r, angleSin * r, 2, i, el)
            gun.reparentTo(self.render)
            self.guns.append(gun)

    def add_terrain(self):
        self.scene = self.loader.loadModel("model_territory/terrain3")
        self.scene.setScale(2)
        self.scene.setZ(-3)
        # print("size"+str(self.scene.getTightBounds()))
        # #size(LPoint3f(-27.241, -28.0331, 0.958751), LPoint3f(28.117, 27.3249, 0.958751))
        self.scene.reparentTo(self.render)

    def camera_set(self):
        self.camera.setPos(0, -50, 230)
        x = 0
        y = -70
        z = 0
        self.camera.setHpr(x, y, z)

    def add_light(self):
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLight.setShadowCaster(True, 512, 512)
        test = self.render.attachNewNode(directionalLight)  #
        test.setHpr(0, 90, 0)
        self.render.setLight(test)

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((0.2, 0.2, 0.2, 0.5))
        self.render.setLight(self.render.attachNewNode(ambientLight))

    def background_image(self, image):
        bgTexture = self.loader.loadTexture(image)  # Load the background texture

        # Make a texture stage for the screen contents and set it to a decal overlay mode
        screenStage = TextureStage('screen')
        screenStage.setMode(TextureStage.MDecal)

        # Make a textre for the screen and a buffer to pipe the screen content into
        self.screenTexture = Texture()
        self.buffer = self.win.makeTextureBuffer("screen buffer", self.win.getXSize(), self.win.getYSize(),
                                                 self.screenTexture, True)
        bufferCam = self.makeCamera(self.buffer, lens=self.cam.node().getLens())

        self.shootTimeDelay = 0.3
        self.shootTimeDelayNow = 0
        # Create a card in render2d to cover up render. Multitexture the card with the BG texture and the screen content texture
        cm = CardMaker('screencard')
        cm.setFrameFullscreenQuad()
        cm.setHasUvs(True)
        screenCard = self.render2d.attachNewNode(cm.generate())
        screenCard.setTexture(bgTexture)
        screenCard.setTexture(screenStage, self.screenTexture)

    def move_camera(self, task):

        speedcharater = 1

        if self.keyMap["left"]:
            self.camera.setX(self.camera.getX() - speedcharater)

        if self.keyMap["right"]:
            self.camera.setX(self.camera.getX() + speedcharater)

        if self.keyMap["forward"]:
            self.camera.setY(self.camera.getY() + speedcharater)

        if self.keyMap["backward"]:
            self.camera.setY(self.camera.getY() - speedcharater)

        return task.cont

    def collision(self, task):
        self.traverser.traverse(self.render)
        for entry in self.queue.getEntries():
            fromnode = str(entry.getFromNodePath())
            intonode = str(entry.getIntoNodePath())

            if fromnode.split('/')[-3] != intonode.split('/')[-3] and 'player' in [fromnode.split('/')[-3],
                                                                                   intonode.split('/')[-3]]:
                # print(fromnode.split('/')[-3], intonode.split('/')[-3],1)
                if intonode.split('/')[-3] == 'Gun':
                    player = fromnode.split('/')[-2]
                    # print(fromnode.split('/')[-3], intonode.split('/')[-3], 2)
                    if task.time - self.players[int(player)].time_pick >= self.players[
                        int(player)].time_delay_pick or not self.players[int(player)].has_a_gun:
                        number_of_gun = intonode.split('/')[-1]
                        # print(fromnode.split('/')[-3], intonode.split('/')[-3], 3)
                        if self.players[int(player)].has_a_gun:
                            # print(fromnode.split('/')[-3], intonode.split('/')[-3], 4.1)
                            self.players[int(player)].gun.get_release()

                        # print(fromnode.split('/')[-3], intonode.split('/')[-3], 4.2)
                        self.players[int(player)].gun = self.guns[int(number_of_gun)]
                        self.players[int(player)].has_a_gun = True
                        self.players[int(player)].time_pick = task.time
                        self.players[int(player)].guntype =self.guns[int(number_of_gun)].type
                        self.guns[int(number_of_gun)].get_pickup(self.players[int(player)].id,
                                                                 self.players[int(player)].getX(),
                                                                 self.players[int(player)].getY(), 5,
                                                                 self.players[int(player)].shoot_decision)

                else:
                    playerhit = fromnode.split('/')[-2]
                    playershoot = intonode.split('/')[-2]
                    shootnumber = intonode.split('/')[-1]
                    copyList = self.players[int(playershoot)].shoot
                    for i, ammo in enumerate(copyList):
                        if ammo.number == int(shootnumber) and (int(playerhit) != int(playershoot)) and not \
                                self.players[int(playershoot)].shoot[i].hit:
                            self.players[int(playershoot)].shoot[i].hit = True
                            self.players[int(playerhit)].health -= self.players[int(playershoot)].shoot[i].dammage
                            self.players[int(playerhit)].player_hit_me = self.players[int(playershoot)].id
                            print("HIIIIIIIIIIIIIIIIIIIIIT  ", self.players[int(playerhit)].id,
                                  self.players[int(playerhit)].health,self.players[int(playerhit)].player_hit_me)

        return task.cont

    def play(self, task):
        # si il ne reste plus que 1 joueur dans le monde du jeu la partie s'arret et le gagnant est révelé
        self.win_or_not()

        # Suppression des joueurs mort et de leur munitions
        self.death_or_not()

        # action des joeurs
        self.agent_action(task.time)

        if self.count_frame >= self.frame_skip:
            self.count_frame = -1
        self.count_frame += 1
        return task.cont

    def win_or_not(self):
        winornot = len(self.playerwin) == 1
        if winornot:
            winnernumber = int(self.playerwin[0])
            print(str(self.players[winnernumber].id) + " a gagné avec " + str(
                self.players[winnernumber].health) + " points de vie")
            sys.exit()
        return winornot

    def death_or_not(self):
        copy_list = self.players
        for (i, el) in enumerate(copy_list):
            if i not in self.playersloose:
                if el.get_health() <= 0:
                    self.players[el.player_hit_me].kill+=1
                    if el.has_a_gun:
                        self.players[i].gun.get_release()
                    self.players[i].erase_ammo()
                    self.players[i].delete()
                    self.playersloose.append(i)
                    self.playerwin.remove(i)
                    print("Player " + str(i) + " est mort")

    def agent_action(self, time):
        old_scores = self.scores.copy()
        old_scores_list = list(self.scores)
        #print(old_scores)
        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if self.count_frame >= self.frame_skip:
                    #print(self.list_agent[i].playerid)
                    '''AGENT ACTION'''
                    self.set_unique_id(i,el.getX(), el.getY())
                    if i == 0:
                        self.set_unique_id_vec(i)
                    action = self.list_agent[i].act(gs=self)

                    '''try:
                        print(self.list_agent[i].Q)
                    except:
                        pass'''

                    shoot_or_not = 1 if action >= 24 else 0
                    action_second = action - 24 if action >= 24 else action

                    random_cut = action_second % 8
                    power_move = int(action_second/8)
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
                    el.shoot_decision = thetashoot

                    el.setHpr((-90 + el.shoot_decision * (180 / pi), 0, 0))

                el.move()
                el.attack(render=self.render, time=time)
                el.ammoshoot(time=time)
                position = (int(el.getX() / 10) + 10) * 21 + (int(el.getY() / 10) + 10)
                position_str = '0' * (3 - len(str(position))) + str(position)
                if position_str not in el.discovery:
                    el.discovery.append(position_str)

                self.scores[i] =  el.kill*500 + el.ammo_hit*20 + len(el.discovery)*10   + (50 -el.health)*10  - el.ammo_miss*1
                #print(len(el.discovery))
                #print("X :",int(el.getX()),",X~ :",int(el.getX()/10),"Y :",int(el.getY()),"Y~ :", int(el.getY()/10), "Number case =",(int(el.getX()/10)+10)*21+(int(el.getY()/10)+10))

        new_scores = self.scores
        rewards = new_scores - old_scores
        #print(new_scores,old_scores)
        #print(self.list_agent)
        print(self.scores)
        for i, agent in enumerate(self.list_agent):
            agent.observe(rewards[i], self.is_game_over(), i)

        #print("---------")


if __name__ == '__main__':
    #Game = BattleRoyale()
    #Game.run()
    for i in range(-100,100):
        for j in range(-100,100):
            position = (int(i / 10) + 10) * 21 + (int(j / 10) + 10)
            position_str = '0' * (3 - len(str(position))) + str(position)
            print(i , j ,position_str)
