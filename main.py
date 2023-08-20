#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Coin game

This is an example of a simple game where you collect coins and avoid enemies.

Made with Python 3.11 and pygame 2.4.

This game was made by Lauri Kenttä in 2023 and is freely available under the terms of The Unlicense. Images embedded in the code are available under the CC0 license.
"""

import io, pygame, random, base64

class Sprite:
    __images = {}
    _image = None

    def __init__(self, x, y, image_file = None, image = None):
        self.set_xy(x, y)
        if image:
            self.image = image
        else:
            key = image_file or self._image
            if not key:
                raise ValueError("No image given")
            if key not in self.__images:
                self.__images[key] = pygame.image.load(image_file or io.BytesIO(base64.b64decode(self._image))).convert_alpha()
            self.image = self.__images[key]

    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def is_at(self, x, y):
        return self.x == x and self.y == y

    def collides_with(self, other, dx = 0, dy = 0):
        return other.is_at(self.x + dx, self.y + dy)

    def draw(self, surface):
        surface.blit(self.image, (self.x * 32, self.y * 32))

class Wall(Sprite):
    # Wall tile, by Lauri Kenttä, under CC0
    _image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAAFVBMVEU3BASJAyiOBgWXESJ+HgKgIgCQKADfg/QQAAABbElEQVQoU12RwXLrIAxFidNmHZlM17HArANKvU6JhnXHHrPuc4D//4Qnd1ntdOaKeyWU+lsdlLR5uLR1ncnjQ72Bay9kbk9GIvdQHWnHEREhbK6Wh3qf/efGMQjybEAUT1pn6Zg3AJh+1NH0No4LofsXiaaHOmjkmCrN6QWaWEa0B2aj0S2XuOJVnRAtP0ED0kcN5qY6yxGI0A599IhndSoxmPtYfqPs4BiovT4z5bYKmM/qAFRYoo6LeJe22xJAkGw615DF9gAT9zg2g1XS6R30LbW2hnGZtrArArbcRP2igJd4Vcdxs1xpJATwfbqJYohMnnrLjIO+7S5ocIAgPaKAjtOKI/RuzfH+BWfVmUCyX6wET4J9hOyXttxmAO3QfavjamPvUkZwBsfyozp5yuSUn1TqgFYu1hbEiZOB/TPkQKfmNWWOA2gMia7qTU5Ts2QwHj6K7HJqUgLdhpz8XcCcKxV0LQrY3/hb/wEq+V7ryU4rygAAAABJRU5ErkJggg=="

class Floor(Sprite):
    # Floor tile, by Lauri Kenttä, under CC0
    _image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAAFVBMVEWHXUC8YDPMdj3Af0ffikfclk/en2XjKxOTAAAA9ElEQVQoz11R0XXEIAxjhMIEPSddIFxvgMRMEJwF+mD/ESoL2rt3+gEcW5KVEN7xbcCZJYmo4jYKVVULzvZaMOvdO+4qMUZZZ88ZIpGk2OFflhBFVplA4QMcuH2h199JlkFqOz+zcFeH3GJasg0VsrtoY+HR7BUwVjmjPHb5DBttcQRAx+Ymi10cuPoPZCtpLzbYQR99olFltDar4okc8HFkTPGlXnCR8m/DC+IaJMTbOZzrzNtsQ0DYMM8Z7Dxkqydq1Fn+dtlvjGP3gHBP4ozjv+Scn8tXGnNZmM5IWwsSK4N/5dnnn7O5vG/78B1zeUb4jl/EyX4xLUR1kQAAAABJRU5ErkJggg=="

class Coin(Sprite):
    # Coin, by Lauri Kenttä, under CC0
    _image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAAFVBMVEUAAABjTiWGaTOWczCmh0Gsizm8m0g53Rk6AAAAAXRSTlMAQObYZgAAAN1JREFUKFOtjcF1wyAQRKXnBgRqICw455iFBtBuAxFLBYb+SzBPyIl9Tub2P7PDNP1b1Iq3V46Cob4YHfFKIr8mIjFXlOXkdcco0nZ+VkKs0lorOw2ec8lFqNwzjZtLbtyEhDh+DRHuTHnzwmmI9bOXHRGXfayuV9qjo0zybQ6BLgVO1ktOQ0S/BYrJiqRxEhHDxhlKPRvaQ0C0rlb4OMQFrA/JMXg9xGwCOCobKL0cYtI2CSSjzZjowrgEoMyzMM2w3lQPnNwrelHanJOjAv0dlh/RP3rnHqXmN/5THhZCL27L5ydqAAAAAElFTkSuQmCC"

class Enemy(Sprite):
    # Fearsome bot, by Lauri Kenttä, under CC0
    _image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAtElEQVRYw+2X2wqFMAwE9/9/enw7iDQ3m1qOGFiERrvT2BIq1YKklgRFbTVvh/hNimPIagBOGpkPcusAMMxfCTAsdXY8bYL9AZPyvbB3cQhAcCpG8wz83N2tyDwBoeC0uKvp+gV21ciXsk0Xz9oqCTSzQVPm1ydG7m6feAqg3vkwQHDysx0S5SfNvNvTgimOtQKQAOC1AHfUBtCkD0A7IfQB7ITQ3wNIQdt1cm0Xg8jAggjjAOPu9yX8+mZeAAAAAElFTkSuQmCC"

class Player(Sprite):
    # Small person, by Lauri Kenttä, under CC0
    _image = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABHklEQVRYw82X0Q0CIQyGu4UP3psLOJM7uIRT+HRLOI2T1JwJhmvaUsrPRZI/6sG1H20BIYo1Tmq4MUA4gPfr9pN8Vr4jAVgDkCBSCghu9tFowAFaoZ8FQJrhqP4FYMgxWeH2ii87e/kCW1Hw1rzST47d5rJr7gVO3tmKZs/Sy+6KPTZDxjPjaHRbbuWSAqEePiN2L6zLYtUGiX78YbQZL9JmKvqwx3Ht3HJkAMKaC7D9vi6r1jcPoDiUn7OioKahdlqDbJoCUIwXSZj6+SEActZKHeBToEEcBhB1jgZgqwg9Qe8El/u5W7DDJ+NcgQhtz/w8Pb6qB0eNt8YJ2z5ABML7x2Q5bwJEIAKh3I0x7FEKorOw2Ehr6jaMuluq7QMavVDl37s4hgAAAABJRU5ErkJggg=="

class Game:
    def __init__(self, level = 0):
        self.map = [
            "####################",
            "#    .     9    5#.#",
            "# 3  # 1 7    9 9..#",
            "#        ..#     #.#",
            "#  9     ###...  #.#",
            "#     9  .9 .p.  #.#",
            "#.#    ###  ...   9#",
            "#     9...98####   #",
            "#9 92  ### 9....9  #",
            "#.#..  .##  ####   #",
            "#.#.#.     1  ##   #",
            "#.#.##  4    9   9 #",
            "#969  9    #       #",
            "#       9  . 9     #",
            "####################"
        ]
        self.sprites = []
        self.walls = [Wall(x, y) for y, row in enumerate(self.map) for x, c in enumerate(row) if c == "#"]
        self.floors = [Floor(x, y) for y, row in enumerate(self.map) for x, c in enumerate(row) if c != "#"]
        self.coins = [Coin(x, y) for y, row in enumerate(self.map) for x, c in enumerate(row) if c != "#" and c != "p" and c != "."]
        self.enemies = [Enemy(x, y) for y, row in enumerate(self.map) for x, c in enumerate(row) if c.isdigit() and int(c) <= level]
        self.player = [Player(x, y) for y, row in enumerate(self.map) for x, c in enumerate(row) if c == "p"][0]
        self.smell = []
        self.level = level
        self.ended = False
        self.completed = False
        self.changed = True
        for i in range(10):
            self.spread_smell()

    def get_smell(self, x, y):
        if x < 0 or y < 0 or y >= len(self.smell) or x >= len(self.smell[y]) or self.map[y][x] == "#" or any(enemy.is_at(x, y) for enemy in self.enemies):
            return 0
        return self.smell[y][x]

    def spread_smell(self):
        new_smell = []
        k = 0.9 ** self.level
        for y, row in enumerate(self.map):
            new_smell.append([])
            for x, c in enumerate(row):
                new_smell[y].append(
                    3/8 * self.get_smell(x, y)
                    + 1/8 * (self.get_smell(x - 1, y) + self.get_smell(x + 1, y) + self.get_smell(x, y - 1) + self.get_smell(x, y + 1))
                    * k
                )
        new_smell[self.player.y][self.player.x] += 1
        self.smell = new_smell

    def move_enemies(self):
        for enemy in self.enemies:
            if random.randint(0, 5 * self.level) == 0:
                continue
            max_smell = 0
            max_direction = (0, 0)
            for direction in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                dx, dy = direction
                smell = random.randint(0, 5 * self.level) and self.get_smell(enemy.x + dx, enemy.y + dy)
                if smell > max_smell and not any(enemy.collides_with(other, dx, dy) for other in self.enemies):
                    max_smell = smell
                    max_direction = direction
            enemy.move(*max_direction)
            if enemy.collides_with(self.player):
                self.ended = True

    def action(self, direction):
        if self.ended:
            return
        dx, dy = direction
        if any(self.player.collides_with(wall, dx, dy) for wall in self.walls):
            dx = dy = 0
        self.player.move(dx, dy)
        self.changed = True
        if any(self.player.collides_with(enemy) for enemy in self.enemies):
            self.ended = True
            return
        for coin in filter(lambda coin: self.player.collides_with(coin), self.coins):
            self.coins.remove(coin)
            if self.coins == []:
                self.ended = True
                self.completed = True
                return
            break
        for i in range(self.level):
            self.spread_smell()
        self.move_enemies()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for sprite in self.walls + self.floors + self.coins + [self.player] + self.enemies:
            sprite.draw(screen)
        pygame.display.set_caption(f"Coin game - level {self.level}, coins left {len(self.coins)}")
        screen.blit(pygame.font.SysFont("Arial", 20).render(f"Level {self.level}, coins left {len(self.coins)}", True, (128, 255, 160)), (5, 6))
        if self.completed:
            screen.blit(pygame.font.SysFont("Arial", 20).render("Level completed! Press space to continue", True, (128, 255, 160)), (228, 6))
        elif self.ended:
            screen.blit(pygame.font.SysFont("Arial", 20).render("Game over! Press space to restart", True, (255, 160, 128)), (228, 6))
        else:
            screen.blit(pygame.font.SysFont("Arial", 20).render("Move with WASD / arrows, skip with space", True, (128, 160, 255)), (228, 6))
        pygame.display.flip()
        self.changed = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((w := 640, h := 480))

    game = Game(1)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_l:
                    game = Game(game.level + 1)
                    continue
                if game.ended:
                    if event.key == pygame.K_SPACE:
                        game = Game(game.level + (1 if game.completed else 0))
                    continue
                key_to_direction = {
                    pygame.K_w: (0, -1),
                    pygame.K_a: (-1, 0),
                    pygame.K_s: (0, 1),
                    pygame.K_d: (1, 0),
                    pygame.K_UP: (0, -1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_RIGHT: (1, 0),
                    pygame.K_SPACE: (0, 0)
                }
                if event.key in key_to_direction:
                    game.action(key_to_direction[event.key])

        if game.changed:
            game.draw(screen)
        clock.tick(60)

if __name__ == "__main__":
    main()
