import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from pygame import font

#intialise le jeu
pygame.init()
font = pygame.font.SysFont('arial', 25)


# font = pygame.font.SysFont('arial', 25)

#creer les directions
#utlise enum pour affecter les chiffres avec variables capitalisees
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
# implimenté en dur
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN1 = (0,255,0)

BLOCK_SIZE = 20
#vitesse du jeu
SPEED = 100


class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # Creer l'affichage
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake') # titre
        self.clock = pygame.time.Clock() # cree la vitesse du jeu
        self.reset()

    def reset(self):
        # reinitialise le jeu
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(1, (self.w-20 - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(1, (self.h-20 - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        # ne pas placer la pomme dans l'interieur du snake
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. prend en compte l'action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. le serpent se deplace
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. verifie si le jeu est terminé
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop() #retire le dernier block du seprent, pour qu'il ne grandisse pas

        # 5. pour le gui et l'horloge
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. retourne game over et score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w-20 - BLOCK_SIZE or pt.x < 20 or pt.y > self.h-20 - BLOCK_SIZE or pt.y < 20:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        """for i in range (0,self.w,20):
            for i_y in range (0,self.h,20):
                if i==0 or i==(self.w-20) and i_y == 0 or i_y == (self.h-20) :
                    pygame.draw.rect(self.display, BLUE1, (i,i_y,self.h-460,self.w))


        for i_a in range (0, self.w,20):
            pygame.draw.rect(self.display, BLUE1, (i_a, 0, self.w, self.h-460))"""



        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [540, 0])
        pygame.display.flip() # update l'affichage

    def _move(self, action):
        # action = [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # ne change pas
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)