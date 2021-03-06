import math

import pygame as pg
import pymunk as pm
from pymunk import Vec2d


def flipy(p):
    """Convert chipmunk coordinates to pg coordinates."""
    return Vec2d(p[0], -p[1]+600)


class Ball(pg.sprite.Sprite):
    def __init__(self, loc, space):
        pg.sprite.Sprite.__init__(self)
        #self.name = name
        self.sizex = 25
        self.sizey = 25
        #self.image = pg.transform.scale(pg.image.load('ball.png'), (self.sizex,self.sizey))
        #self.rect = self.image.get_rect()
        self.image = pg.Surface((self.sizex, self.sizey), pg.SRCALPHA)
        pg.draw.circle(self.image, pg.Color('steelblue2'), (self.sizex, self.sizey), 29)
        self.rect = self.image.get_rect(center=loc)
        self.orig_image = self.image
        #self.rect.inflate(-30,-30)
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        self.body = pm.Body()
        self.shape = pm.Circle(self.body, radius=30)
        self.shape.density = .0001
        self.shape.friction = .1
        self.shape.elasticity = .99
        self.body.position = loc
        self.space = space
        self.space.add(self.body, self.shape)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.accel_forw = True
            if event.key == pg.K_a:
                self.turn_left = True
            if event.key == pg.K_d:
                self.turn_right = True
            if event.key == pg.K_s:
                self.accel_back = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.accel_forw = False
            if event.key == pg.K_a:
                self.turn_left = False
            if event.key == pg.K_d:
                self.turn_right = False
            if event.key == pg.K_s:
                self.accel_back = False

    def update(self, dt):
    #     # Accelerate the pm body of this sprite.
    #     # if self.accel_forw and self.body.velocity.length < self.topspeed:
    #     #     self.body.apply_force_at_local_point(Vec2d(0, 624), Vec2d(0, 0))
    #     # if self.accel_back and self.body.velocity.length < self.topspeed:
    #     #     self.body.apply_force_at_local_point(Vec2d(0, -514), Vec2d(0, 0))
    #     # if self.turn_left and self.body.velocity.length < self.topspeed:
    #     #     self.body.angle += .1
    #     #     self.body.angular_velocity = 0
    #     # if self.turn_right and self.body.velocity.length < self.topspeed:
    #     #     self.body.angle -= .1
    #     #     self.body.angular_velocity = 0
    #     # Rotate the image of the sprite.
    #     self.angle = self.body.angle
    #     self.rect.center = flipy(self.body.position)
    #     self.image = pg.transform.rotozoom(
    #         self.orig_image, math.degrees(self.body.angle), 1)
        self.rect = self.image.get_rect(center=self.rect.center)


class Wall(pg.sprite.Sprite):

    def __init__(self, pos, verts, space, mass, *sprite_groups):
        super().__init__(*sprite_groups)
        # Determine the width and height of the surface.
        width = max(v[0] for v in verts)
        height = max(v[1] for v in verts)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.polygon(self.image, pg.Color('sienna1'), verts)
        self.rect = self.image.get_rect(topleft=pos)

        moment = pm.moment_for_poly(mass, verts)
        self.body = pm.Body(mass, moment, pm.Body.STATIC)
        # Need to transform the vertices for the pm poly shape,
        # so that they fit to the image vertices.
        verts2 = [(x, -y) for x, y in verts]
        self.shape = pm.Poly(self.body, verts2, radius=2)
        self.shape.friction = 0.1
        self.shape.elasticity = .92
        self.body.position = flipy(pos)
        self.space = space
        self.space.add(self.shape)


class Game:

    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color(0, 0, 0)

        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, 0.0)
        self.space.damping = .4

        self.all_sprites = pg.sprite.Group()

        self.ball = Ball((300, 300), self.space)
        #self.ball2 = Ball((400, 300), self.space)
        self.all_sprites.add(self.ball)
        # Position and vertices tuples for the walls.
        # vertices = [
        #     ([10, 80], ((0, 0), (200, 0), (90, 500), (0, 500))),
        #     ([400, 250], ((40, 80), (200, 0), (170, 90), (10, 170))),
        #     ([600, 450], ((20, 40), (300, 0), (300, 120), (10, 100))),
        #     ([760, 10], ((0, 0), (30, 0), (30, 420), (0, 400))),
        #     ([10, 10], ((0, 0), (760, 0), (700, 60), (0, 60))),
        #     ([10, 580], ((0, 0), (760, 0), (700, 60), (0, 60))),
        #     ]

        # for pos, verts in vertices:
        #     Wall(pos, verts, self.space, 1, self.all_sprites)

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            self.ball.handle_event(event)

    def run_logic(self):
        self.space.step(1/60)
        #self.all_sprites.update(self.dt)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()