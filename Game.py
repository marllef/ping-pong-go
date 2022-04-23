from random import randint

import matplotlib.pyplot as plt
import pygame as pg
import torch
from pygame import display, draw, time, KMOD_CTRL, K_s
from torch import tensor

from IA.Neural.Network import MultiLayerNetwork
from Objects.Ball import Ball
from Objects.Player import Player
from os import path

IA_1 = path.join(path.basename(''), 'IA/Models/', 'Ia_right_defense.pt')
IA_2 = path.join(path.basename(''), 'IA/Models/', 'my_network_neural.pt')


def save(name):
    return path.join(path.basename(''), 'IA/Models/', name)


class Game:
    def __init__(self, name='Ping Pong Go'):
        pg.init()
        self.bg_color = [255, 255, 255]
        self.ia_treino = MultiLayerNetwork([3, 255, 1])
        self.ia_treino.load_state_dict(torch.load(IA_1))
        self.ia_treino.eval()
        # self.ia_treino.train()

        self.ia = MultiLayerNetwork([3, 255, 1])
        # self.ia2 = MultiLayerNetwork([4, 255, 150, 1])
        self.ia.load_state_dict(torch.load(IA_2))
        self.ia.eval()

        self.clock = time.Clock()
        self.player = Player()
        self.player_treino = Player(pos=(710, 200))
        self.ball = Ball()
        self.display = display.set_mode([720, 400])
        self.quit = False
        display.set_caption(name)

    def run(self):
        while not self.quit:
            self.__draw()
            self.__update()
            self.__events_observer()

    def __draw(self):
        self.display.fill(self.bg_color)
        draw.rect(self.display, [0, 0, 0], self.player)
        draw.rect(self.display, [0, 0, 0], self.player_treino)
        draw.rect(self.display, self.ball.color, self.ball)

    def __update(self):
        self.ball.update([self.player, self.player_treino])

        # params_treino = tensor([[[self.player_treino.rect.y], [self.ball.rect.x], [self.ball.rect.y], [self.ball.p2_win]]])
        params_ia_1 = tensor([self.player_treino.rect.y, self.ball.rect.x, self.ball.rect.y])
        params_ia_2 = tensor([self.player.rect.y, self.ball.rect.x, self.ball.rect.y])

        if self.ball.p2_win:
            self.ball.color = [0, randint(40, 200), randint(40, 200)]
            self.ball.p2_win = False

        # prediction = self.ia_treino.play(params_treino, learning_rate=0.01)
        ia_1_command = self.ia_treino(params_ia_1)
        ia_2_command = self.ia(params_ia_2)

        self.player.update(ia_2_command.item())
        self.player_treino.update(ia_1_command.item())

        # self.clock.tick(200)
        display.update(self.display.get_rect())

    def __events_observer(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
                pg.quit()
            if keys[K_s]:
                print('Rede salva com sucesso!')
                torch.save(self.ia_treino.state_dict(), save('Ia_right_defense.pt'))
                # torch.save(self.ia.state_dict(), save('Ia_2.pt'))


game = Game()

game.run()
