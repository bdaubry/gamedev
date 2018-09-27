import sys, pygame, classes, pymunk
from pymunk import Vec2d

pygame.init()

size = width, height = 800, 600
move_spd = 4
speed = [0, 0]
gravity = [0, -5]
black = 0, 0, 0
pygame.key.set_repeat(5,5)
balltotal = 0
ballname = 'ball'+str(balltotal)
space = pymunk.Space()
space.gravity = Vec2d(0.0, 0.0)
space.damping = .4

activeball = pygame.sprite.Group()
ballgroup = pygame.sprite.Group()

screen = pygame.display.set_mode(size)
balls = [] 

def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)

player = classes.Player()
#ball = classes.Ball() 

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                speed[0] = -move_spd
            if event.key == pygame.K_d:
                speed[0] = move_spd
            if event.key == pygame.K_s:
                speed[1] = move_spd
            if event.key == pygame.K_w:
                speed[1] = -move_spd
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                speed[0] = 0
            if event.key == pygame.K_d:
                speed[0] = 0
            if event.key == pygame.K_s:
                speed[1] = 0
            if event.key == pygame.K_w:
                speed[1] = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            active = classes.Ball(pygame.mouse.get_pos(), ballname)
            activeball.add(active)

        if event.type == pygame.MOUSEBUTTONUP:
            for x in activeball:
                ballgroup.add(x)
            activeball.empty()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            active = classes.Ball(mouse_pos, space)
            activeball.add(active)
            #balltotal += 1

                
    player.rect = player.rect.move(speed)

    if player.rect.left < 0: 
        player.rect.left = 0
    if player.rect.right > width:
        player.rect.right = width
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > height:
        player.rect.bottom = height

    for ball in activeball:
        if pygame.mouse.get_pressed():
            ball.grow(True)
        else:
            ball.grow(False)
        # elif pygame.mouse.get_pressed() == False:
        #     ball.grow(False)

    for ball in ballgroup:
        ball.grow(False)
        # ballhit = pygame.sprite.collide_rect(player, ball)
        # if ballhit:
        #     balls.pop()
        if ball.rect.bottom < height:
            ball.rect.y = ball.rect.y - gravity[1]
        elif ball.rect.bottom == height:
            ball.rect.y = height
        
    screen.fill(black)
    for x in activeball.sprites():
        screen.blit(x.image, x.rect.topleft)
    for x in ballgroup.sprites():
        screen.blit(x.image, x.rect.topleft)

    screen.blit(player.image, player.rect)
    pygame.display.flip()