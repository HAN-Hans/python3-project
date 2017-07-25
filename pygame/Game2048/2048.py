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



class Map(object):
    """docstring for Map"""
    def __init__(self, size = SIZE, win = 128):
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

    # 矩阵值为零单元随机生成一个2或4
    def add(self):
        new_element = 4 if random.randrange(100) > 85 else 2
        (i,j) = random.choice([(i,j) for i in range(self.size) for j in range(self.size) if self.matrix[i][j] ==0]) 
        self.matrix[i][j] = new_element

    def is_win(self):
        return any(any((i > self.win_value) for i in row) for row in self.matrix)

    def is_over(self):
        for r in range(self.size):  
            for c in range(self.size):  
                if self.matrix[r][c] == 0:  
                    return False  
        for r in range(self.size):  
            for c in range(self.size - 1):  
                if self.matrix[r][c] == self.matrix[r][c + 1]:  
                    return False  
        for r in range(self.size - 1):  
            for c in range(self.size):  
                if self.matrix[r][c] == self.matrix[r + 1][c]:  
                    return False  
        return True

    # 矩阵单元显示
    def drawBlock(self, screen, row, column, color, blocknum):
        font = pygame.font.SysFont('stxingkai', 80)
        w = column * PIXEL + (column + 1) * GAP
        h = row * PIXEL + (row + 1) * GAP + PIXEL
        block_rect = pygame.Rect(w, h, PIXEL, PIXEL)
        pygame.draw.rect(screen, color, block_rect)
        if blocknum != 0:
            fw,fh = font.size(str(int(blocknum)))
            screen.blit(font.render(str(int(blocknum)), 1, (0,0,0)), (w+(PIXEL-fw)/2, h+(PIXEL-fh)/2))

    # 界面显示
    def drawSurface(self, screen):
        help_string1 = '(Q)Exit   (W)Up   (R)Restart'
        help_string2 = '(S)Down (row)Left (D)Right'
        over_string = 'GAME OVER'
        win_string = 'YOU WIN!'

        title_rect = pygame.Rect(0, 0, screen_width, PIXEL)
        pygame.draw.rect(screen, (250, 250, 250), title_rect)
        font1 = pygame.font.SysFont('simsun', 48)
        font2 = pygame.font.SysFont('Georgia', 20)
        font3 = pygame.font.SysFont('Georgia', 35)
        screen.blit(font1.render('Score:', 1, (255,127,10)), (20,15))
        screen.blit(font1.render('%s' % self.score, 1, (255,127,10)), (125,15))
        screen.blit(font1.render('Best:', 1, (255,127,10)), (20,65))
        screen.blit(font1.render('%s' % self.highscore, 1, (255,127,10)), (125,65))

        for i in range(self.size):
            for j in range(self.size):
                self.drawBlock(screen, i, j, BLOCK_COLORS[self.matrix[i][j]], self.matrix[i][j])

        if self.is_win():
            screen.blit(font3.render(win_string, 1, (10,10,10)), (225,30))
        elif self.is_over():
            screen.blit(font3.render(over_string, 1, (10,10,10)), (225,30))
        else:
            screen.blit(font2.render(help_string1, 1, (255,127,10)), (225,20))
            screen.blit(font2.render(help_string2, 1, (255,127,10)), (225,60))

    def invert(self):         # 矩阵逆转
        self.matrix =  [row[::-1] for row in self.matrix]
    
    def transpose(self):      # 矩阵转置
        t = []
        for i in (zip(*self.matrix)):
            t.append(list(i))
        self.matrix = t

    # 将矩阵非零项向左挤，并且合并相同项 ，其他方向的可以适当调整实现
    # 返回一个changed，为faise说明不可移动，True则表明可移动
    def move_is_possible(self):  
        changed = False  
        for row in self.matrix:  
            nwe_row = []  
            last = 0  
            for i in row:  
                if i != 0:  
                    if i == last:  
                        nwe_row.append(2 * nwe_row.pop()) 
                        self.score += 2 * i
                        last = 0  
                    else:  
                        nwe_row.append(i)  
                        last = i  
            nwe_row += [0] * (len(row) - len(nwe_row))  
            for i in range(self.size):  
                if row[i] != nwe_row[i]:  
                    changed = True  
            row[:] = nwe_row  
        return changed 

    def moveLeft(self):
        if self.move_is_possible():
            self.add()

    def moveRight(self):
        self.invert()
        if self.move_is_possible():
            self.add()
        self.invert() 
       
    def moveUp(self):
        self.transpose()
        if self.move_is_possible():
            self.add()
        self.transpose() 

    def moveDown(self):
        self.transpose()
        self.invert()
        if self.move_is_possible():
            self.add()
        self.invert()
        self.transpose()

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
            else:
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

