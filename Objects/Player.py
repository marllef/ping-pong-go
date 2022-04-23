from pygame import rect, key, K_UP, K_DOWN, display


class Player:
    def __init__(self, pos=(0, 0), size=(10, 70)):
        self.speed = 5
        self.display = display.get_surface()
        self.rect = rect.Rect(pos, size)

    def update(self, command, human=False):
        keys = key.get_pressed()
        if not human:
            if 0 <= self.rect.y:
                if int(command) > self.rect.centery:

                    self.rect.y -= self.speed if self.rect.y != 0 else 0

            if self.rect.y < 400 - self.rect.h:
                if int(command) < self.rect.centery:
                    self.rect.y += self.speed if self.rect.y != 400 - self.rect.h else 0
        else:
            if 0 <= self.rect.y:
                if keys[K_UP]:
                    self.rect.y -= self.speed if self.rect.y != 0 else 0

            if self.rect.y < display.get_surface().get_rect().h - self.rect.h:
                if keys[K_DOWN]:
                    self.rect.y += self.speed if self.rect.y != 400 - self.rect.h else 0
