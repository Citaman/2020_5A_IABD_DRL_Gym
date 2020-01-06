import random
import sys
import numpy as np
from math import cos, sin, pi

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
# AmbientLight, DirectionalLight, CollisionHandlerQueue, CollisionTraverser, Camera, NodePath, Texture, TextureStage,
# CardMaker
# from direct.gui.OnscreenImage import OnscreenImage
# from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionSphere, CollisionCapsule

from environments.battle_royale.game import Player, Gun


class BattleRoyalGameWorld(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.keyMap = {"left": False, "right": False, "forward": False, "backward": False, "shoot": False}
        self.players = []
        self.guns = []
        self.traverser = CollisionTraverser('traverser name')
        self.queue = CollisionHandlerQueue()
        self.playersloose = []
        self.numberofGun = 8
        self.numberofPlayer = 6
        self.playerwin = [i for i in range(self.numberofPlayer)]
        self.time2 = 0
        self.frame_skip = 15
        self.count_frame = 15
        self.level = 0
        self.action_space_movement = 8
        self.action_space_direction = 2
        self.action_space_shoot_yes_or_not = 2

        self.action()

        self.addterrain()

        self.addlight()

        self.backgroundImage("../clear-blue-sky.jpeg")

        self.addPlayer()

        self.addGun()

        self.disableMouse()

        self.cameraset()
        # self.splitScreen(self.cam, self.displayRegion2())

        self.taskMgr.add(self.movethecamera, "movecamera")
        self.taskMgr.add(self.colision, "colision")
        self.taskMgr.add(self.play, "play")

    def action(self):
        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["backward", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["backward", False])
        self.accept("space", self.setKey, ["shoot", True])
        self.accept("space-up", self.setKey, ["shoot", False])

    def setKey(self, key, value):
        self.keyMap[key] = value

    def addPlayer(self):
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

    def addGun(self):
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

    def addterrain(self):
        self.scene = self.loader.loadModel("../model_territory/terrain3")
        self.scene.setScale(2)
        self.scene.setZ(-3)
        # print("size"+str(self.scene.getTightBounds()))
        # #size(LPoint3f(-27.241, -28.0331, 0.958751), LPoint3f(28.117, 27.3249, 0.958751))
        self.scene.reparentTo(self.render)

    def cameraset(self):
        self.camera.setPos(0, -50, 230)
        x = 0
        y = -70
        z = 0
        self.camera.setHpr(x, y, z)

    def addlight(self):
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
        '''

        directionalLight2 = DirectionalLight("directionalLight2")
        directionalLight2.setDirection((5, -5, 5))
        directionalLight2.setColor((1, 1, 1, 1))
        self.render.setLight(self.render.attachNewNode(directionalLight2))

        directionalLight2 = DirectionalLight("directionalLight3")
        directionalLight2.setDirection((0, 5, 5))
        directionalLight2.setColor((1, 1, 1, 1))
        self.render.setLight(self.render.attachNewNode(directionalLight2))

        directionalLight2 = DirectionalLight("directionalLight4")
        directionalLight2.setDirection((5, 5, 5))
        directionalLight2.setColor((1, 1, 1, 1))
        self.render.setLight(self.render.attachNewNode(directionalLight2))
        '''

    def backgroundImage(self, image):
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

    def movethecamera(self, task):

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

    def colision(self, task):
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
                            print("HIIIIIIIIIIIIIIIIIIIIIT  ", self.players[int(playerhit)].id,
                                  self.players[int(playerhit)].health)

        return task.cont

    def play(self, task):
        # si il ne reste plus que 1 joueur dans le monde du jeu la partie s'arret et le gagnant est révelé
        self.win_or_not()

        # Suppression des joueurs mort et de leur munitions
        self.death_or_not()

        # action des joeurs
        self.agentAction(task.time)

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
                    if el.has_a_gun:
                        self.players[i].gun.get_release()
                    self.players[i].erase_ammo()
                    self.players[i].delete()
                    self.playersloose.append(i)
                    self.playerwin.remove(i)
                    print("Player " + str(i) + " est mort")

    def agentAction(self, time):
        for (i, el) in enumerate(self.players):
            if i not in self.playersloose:
                if self.count_frame >= self.frame_skip:
                    random_cut = random.choice(list(range(self.action_space_movement+1)))
                    theta_move = (2 * pi / (self.action_space_movement)) * (random_cut)  # random.uniform(0,2*pi)
                    power_move = random.choice(list(range(self.action_space_direction+1)))
                    #print( "random cut",random_cut,"power", power_move)
                    el.X_decision = cos(theta_move) * power_move/2
                    el.Y_decision = sin(theta_move) * power_move/2

                    if self.level > 0:
                        random_cut2 = random.choice(list(range(17)))
                        thetashoot = (2 * pi / (16)) * (random_cut2)
                    else:
                        #random_cut2 = random_cut
                        thetashoot = theta_move
                    el.shoot_decision = thetashoot
                    el.shoot_or_not_decision = random.random()
                    el.setHpr((-90 + el.shoot_decision * (180 / pi), 0, 0))
                    # print(el.getHpr())

                el.move()
                el.attack(render=self.render, time=time)
                el.ammoshoot(time=time)

if __name__ == '__main__':
    Game1 = BattleRoyalGameWorld()
    Game1.run()
