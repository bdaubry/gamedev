import math

import pygame as pg
import pymunk as pm
from pymunk import Vec2d


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)

class Ball(pg.sprite.Sprite):
    def __init__(self, pos, space):
        super().__init__()
        self.image = pg.Surface((60, 60), pg.SRCALPHA)
        self.radius = 29
        pg.draw.circle(self.image, pg.Color('steelblue2'), (30,30), self.radius)
        self.rect = self.image.get_rect(center=pos)
        self.orig_image = self.image
        # Create the physics body and shape of this object.
        self.mass = 100
        self.inertia = pm.moment_for_circle(self.mass, 0, self.radius, (0,0))
        self.body = pm.Body(self.mass, self.inertia)
        self.shape = pm.Circle(self.body, radius=30)
        self.shape.density = .0001
        self.shape.friction = .1
        self.shape.elasticity = .99
        self.body.position = flipy(pos)
        # Add them to the Pymunk space.
        self.space = space
        self.space.add(self.body, self.shape)
        print(self.body.mass)

        self.accel_forw = False
        self.accel_back = False
        self.turn_left = False
        self.turn_right = False
        self.topspeed = 1790
        self.angle = 0

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
        # Accelerate the pymunk body of this sprite.
        if self.accel_forw and self.body.velocity.length < self.topspeed:
            self.body.apply_force_at_local_point(Vec2d(0, 624), Vec2d(0, 0))
        if self.accel_back and self.body.velocity.length < self.topspeed:
            self.body.apply_force_at_local_point(Vec2d(0, -514), Vec2d(0, 0))
        if self.turn_left and self.body.velocity.length < self.topspeed:
            self.body.angle += .1
            self.body.angular_velocity = 0
        if self.turn_right and self.body.velocity.length < self.topspeed:
            self.body.angle -= .1
            self.body.angular_velocity = 0
        # Rotate the image of the sprite.
        self.angle = self.body.angle
        self.rect.center = flipy(self.body.position)
        self.image = pg.transform.rotozoom(
            self.orig_image, math.degrees(self.body.angle), 1)
        self.rect = self.image.get_rect(center=self.rect.center)

class MainBall(pg.sprite.Sprite):
    def __init__(self, pos, space):
        super().__init__()
        self.radius = 15
        self.diameter = self.radius * 2
        self.pos = pos
        self.image = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
        pg.draw.circle(self.image, pg.Color('steelblue2'), (self.diameter,self.diameter), self.radius)
        self.rect = self.image.get_rect(center=pos)
        self.orig_image = self.image
        # Create the physics body and shape of this object.
        self.mass = 100
        self.inertia = pm.moment_for_circle(self.mass, 0, self.radius, (0,0))
        self.body = pm.Body(self.mass, self.inertia)
        self.shape = pm.Circle(self.body, radius=self.radius)
        self.shape.density = .0001
        self.shape.friction = .1
        self.shape.elasticity = .99
        self.body.position = flipy(self.pos)
        # Add them to the Pymunk space.
        self.space = space
        self.space.add(self.body, self.shape)
        print(self.body.mass)

    def grow(self, growbool):
        self.growbool = growbool
        if self.growbool == True:
            self.radius = self.radius + 2
            self.image = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
            pg.draw.circle(self.image, pg.Color('steelblue2'), (self.diameter,self.diameter), self.radius)
            self.rect = self.image.get_rect(center=self.pos)
        print(self.radius)
            



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
        # Need to transform the vertices for the pymunk poly shape,
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
        self.width = 800
        self.height = 600
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color(60, 60, 60)

        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -1000.0)
        self.space.damping = .4

        self.all_sprites = pg.sprite.Group()
        self.main_sprite = pg.sprite.Group()

        # self.ball = Ball((300, 300), self.space)
        # self.ball2 = Ball((400, 300), self.space)
        
        # Position and vertices tuples for the walls.
        vertices = [
            ([0, 0], ((0, 0), (0, self.height), (5, self.height), (5, 0))),
            ([0, 0], ((0, self.height), (self.width, self.height), (self.width, self.height-5), (0, self.height-5))),
            ([0, -self.height+5], ((0, self.height), (self.width, self.height), (self.width, self.height-5), (0, self.height-5))),
            ([self.width-5, 0], ((0, 0), (0, self.height), (5, self.height), (5, 0))),
            # ([10, 10], ((0, 0), (760, 0), (700, 60), (0, 60))),
            # ([10, 580], ((0, 0), (760, 0), (700, 60), (0, 60))),
            ]

        for pos, verts in vertices:
            Wall(pos, verts, self.space, 1, self.all_sprites)

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
            if event.type == pg.MOUSEBUTTONDOWN:
                #print(pg.mouse.get_pos())
                self.ball = MainBall(pg.mouse.get_pos(), self.space)
                self.main_sprite.add(self.ball)
            #if event.type == pg.MOUSEBUTTONUP:
                # self.balln = Ball(self.ball.body.position,self.space)
                # for ball in self.main_sprite:
                #     self.all_sprites.add(ball)
                #     self.main_sprite.remove(ball)       
        
        for ball in main_sprite:
            if pygame.mouse.get_pressed():
                ball.grow(True)
            else:
                ball.grow(False)
                #self.ball.handle_event(event)

    def run_logic(self):
        self.space.step(1/60)
        self.all_sprites.update(self.dt)
        self.main_sprite.update(self.dt)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.all_sprites.draw(self.screen)
        self.main_sprite.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()