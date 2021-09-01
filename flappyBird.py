import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

# importing images of birds
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(
                 os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]


PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))

BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:

    IMGS = BIRD_IMGS        # different bird images for animation
    MAX_ROTATION = 25       # how mauch degree will the bird turn
    ROT_VEL = 20            # how much the bird will rotate on each frame
    ANIMATION_TIME = 5      # fps of the bird flapping

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):            # for every jump made this functions triggers

        # upwards -velocity
        # downwards +velocity
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # displacement  how many pixels up or down
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        # -10.5 + 1.5 = -9pix
        # this formula results an arc for the bird

        if d >= 16:             # prevent the speed from increasing when moving downwards
            d = 16              # do not increase speed after 16

        if d < 0:
            d -= 2

        self.y = self.y+d         # add to y position for registering into the game

        # animations of the bird
        if d < 0 or self.y < self.height + 50:   # if moving upwards
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        else:                                     # moving downwards
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]

        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]

        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # rotates image from top left (0,0) of the image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)

        # rotates image around the center
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    # space between pipes
    GAP = 200
    # velocity of pipe
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height-self.PIPE_TOP.get_height()

        self.bottom = self.height+self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # offset - how far away these masks are from each other
        top_offset = (self.x-bird.x, self.top-round(bird.y))
        bottom_offset = (self.x-bird.x, self.bottom-round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    # cycling images
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1+self.WIDTH < 0:
            self.x1 = self.x2+self.WIDTH

        if self.x2+self.WIDTH < 0:
            self.x2 = self.x1+self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird):
    # blit=draw
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():

    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)                 # FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(win, bird)

    pygame.quit()
    quit()


main()
