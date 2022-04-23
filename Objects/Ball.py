from random import randint, choice

from pygame import rect, display, key, K_SPACE, time


class Ball:
    def __init__(self, size=(10, 10)):
        self.speed = [-1, choice([-1, 0, 1])]
        self.win = False
        self.p2_win = False

        self.not_reset = True

        self.tick = 0
        self.color = [255, 0, 0]
        pos = [360, randint(60, 340)]
        self.rect = rect.Rect(pos, size)

    def update(self, collide_obj=None):
        keys = key.get_pressed()
        screen = display.get_surface().get_rect()

        # self.tick += 1
        self.__collide(collide_obj)

        self.rect.x -= self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.x == 0:
            print('Ponto do player 2!')
            self.win = True

            if self.speed[1] == 0:
                self.speed[1] = choice([-1, 1])

            self.speed[0] = -self.speed[0]

        if self.rect.x == screen.w - self.rect.w:
            print('Ponto do player 1!')

            self.p2_win = True
            if self.speed[1] == 0:
                self.speed[1] = choice([-1, 1])

            self.speed[0] = -self.speed[0]

        if self.rect.y == 0:
            self.speed[1] = -self.speed[1]

        if self.rect.y + self.rect.h >= screen.h:
            self.speed[1] = -self.speed[1]

        '''
        if keys[K_SPACE]:
            time.Clock().tick(30)
            self.not_reset = not self.not_reset
            print(f'RESETA? {not self.not_reset}')

        if self.tick > 60 * 7 and not self.not_reset:
            self.tick = 0
            self.__init__()
        '''

    def __collide(self, players):

        if players:
            # Player 1 Collision
            if self.rect.colliderect(players[0].rect):
                player_1 = players[0]
                print('Player 1 Defendeu!')
                self.rect.x = player_1.rect.x + player_1.rect.w + 1
                if self.speed[1] == 0:
                    self.speed[1] = choice([-1, 1])

                self.speed[0] = -self.speed[0]

            # Player 2 Collision
            if self.rect.colliderect(players[1].rect):
                player_2 = players[1]
                print('Player 2 Defendeu!')
                self.rect.x = player_2.rect.x - player_2.rect.w - 1
                if self.speed[1] == 0:
                    self.speed[1] = choice([-1, 1])

                self.speed[0] = -self.speed[0]
