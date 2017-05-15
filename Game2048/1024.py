# -*- coding:utf-8 -*-

import pygame, random, sys
from pygame.locals import *

SIZE = 4        # 设置矩阵行列
PIXEL = 110     # 一个单元占用像素点
GAP = 10      # 每个单元的间隙

screen_width = (PIXEL + GAP) * SIZE + GAP
screen_height = screen_width + PIXEL
screen_size = (screen_width, screen_height)

# 设置不同数值矩形框RBG颜色
BLOCK_COLORS = {
    0:(150,150,150),
    2:(255,255,255),
    4:(255,255,128),
    8:(255,255,0),
    16:(255,220,128),
    32:(255,220,0),
    64:(255,190,0),
    128:(255,160,0),
    256:(255,130,0),
    512:(255,100,0),
    1024:(255,70,0),
    2048:(255,40,0),
    4096:(255,10,0)
}   


def invert(matrix):         # 矩阵逆转
    return [row[::-1] for row in matrix]
def transpose(matrix):      # 矩阵转置
    return [list(zip(*matrix))]

# class Move(object):
#     """docstring for Move"""
#     def __init__(self, arg):
#         super(Move, self).__init__()
#         self.arg = arg

#     def move_is_possible(self, direction):
#         def row_left_moveable(row):
#             def is_moveable(i):
#                 if row[i] == 0 and row[i + 1] != 0:         # 可移动
#                     return True
#                 if row[i] != 0 and row[i] == row[i + 1]     # 可合并
#                     return True
#                 retrun False
#             return any(is_moveable(i) for i in (len(row) - 1))

#         check = {}
#         check[]


#     def moveUp():
#         pass

#     def moveDown():
#         pass

#     def moveLeft():
#         matrix = self.matrix.copy()                               #获得一份矩阵的复制
#         newmatrix = self.toSequence(matrix)
#         return newmatrix,self.score


#     def moveRight():
#         pass

class Map(object):
    """docstring for Map"""
    def __init__(self, size = SIZE, win = 2048):
        super(Map, self).__init__()
        self.size = size
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.matrix = [[0 for i in range(self.size)] for j in range(self.size)]
        self.add()
        self.add()

    def add(self):
        new_element = 4 if random.randrange(100) > 85 else 2
        (i,j) = random.choice([(i,j) for i in range(self.size) for j in range(self.size) if self.matrix[i][j] ==0]) 
        self.matrix[i][j] = new_element

    # def is_win(self):
    #     return any(any((i > self.win_value) for i in row) for row in self.matrix)

    # def is_over():
    #     return any(move_is_possible(move) for move in actions)

    def drawBlock(self, screen, row, column, color, blocknum):
        font = pygame.font.SysFont('stxingkai', 80)
        w = column * PIXEL + (column + 1) * GAP
        h = row * PIXEL + (row + 1) * GAP + PIXEL
        block_rect = pygame.Rect(w, h, PIXEL, PIXEL)
        pygame.draw.rect(screen, color, block_rect)
        if blocknum != 0:
            fw,fh = font.size(str(int(blocknum)))
            screen.blit(font.render(str(int(blocknum)), 1, (0,0,0)), (w+(PIXEL-fw)/2, h+(PIXEL-fh)/2))

    def drawSurface(self, screen):
        help_string1 = '(Q)Exit   (W)Up   (R)Restart'
        help_string2 = '(S)Down (A)Left (D)Right'
        gameover_string = 'GAME OVER'
        win_string = 'YOU WIN!'

        title_rect = pygame.Rect(0, 0, screen_width, PIXEL)
        pygame.draw.rect(screen, (250, 250, 250), title_rect)
        font1 = pygame.font.SysFont('simsun', 48)
        font2 = pygame.font.SysFont('Georgia', 20)
        screen.blit(font1.render('Score:', 1, (255,127,10)), (20,25))
        screen.blit(font1.render('%s' % self.score, 1, (255,127,10)), (175,25))
        screen.blit(font2.render(help_string1, 1, (255,127,10)), (225,20))
        screen.blit(font2.render(help_string2, 1, (255,127,10)), (225,60))

        for i in range(self.size):
            for j in range(self.size):
                self.drawBlock(screen, i, j, BLOCK_COLORS[self.matrix[i][j]], self.matrix[i][j])


        # if is_win():
        #     screen.blit(font2.render('win_string', 1, (10,10,10)), (20,20))
        # elif move_is_possible():

              

def main():
    
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('2048')

    map = Map()
    map.drawSurface(screen = screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit() 

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_r]:
            map.reset()
        elif pressed_keys[K_w] or pressed_keys[K_UP]:  
            map.moveUp()  
        elif pressed_keys[K_s] or pressed_keys[K_DOWN]:  
            map.moveDown()  
        elif pressed_keys[K_a] or pressed_keys[K_LEFT]:  
            map.moveLeft()  
        elif pressed_keys[K_d] or pressed_keys[K_RIGHT]:  
            map.moveRight()
        elif pressed_keys[K_q]:
            sys.exit()
        map.drawSurface(screen = screen) 

        # screen.blit(background, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()

