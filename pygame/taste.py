import sys, pygame
pygame.init()

size = width, height = 480, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

background = pygame.image.load('resources/image/background.png').convert()
ball = pygame.image.load("resources/image/ball.gif").convert()
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
        	sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(background, (0, 0))
    screen.blit(ball, ballrect)
    pygame.display.flip()
