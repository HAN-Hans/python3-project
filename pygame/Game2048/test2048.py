#encoding=utf-8
import pygame 
import random 
import numpy 
from pygame.locals import *

SIZE = 4                                                                                 #游戏尺寸
SCORE = 0                                                                                #初始分数
NUM_BLOCK = 110                                                                 #数字块大小
BLOCK_SPACE = 10                                                                 #数字块间隙
H=NUM_BLOCK*SIZE+BLOCK_SPACE*(SIZE+1)                        #界面宽度
TITLE_RECT = pygame.Rect(0,0,H,110)                                #title大小
DATA = numpy.zeros([SIZE,SIZE])                                        #初始数字矩阵
SCREEN_SIZE = (H,H+110)                                                        #界面尺寸
BLOCK_COLOR = {
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
        4096:(255,10,0),
}                                                                                                #数块颜色



class NumUpdata(object):
        """docstring for NumUpdata"""
        def __init__(self,data):
                super(NumUpdata, self).__init__()
                self.data = data
                self.zerolist=[]
                self.score=0
        
        def sumSameNum(self,dl):
                global score
                start_num=0
                end_num=len(dl)-dl.count(0)
                while start_num<end_num-1:
                        if dl[start_num] ==  dl[start_num+1]:
                                dl[start_num]=dl[start_num]*2                                
                                self.score+=dl[start_num]
                                dl[start_num+1:]=dl[start_num+2:]
                                dl.append(0)
                        start_num+=1
                return dl
        
        def removeZero(self,dl):
                while True:
                        mid=dl[:]
                        try:
                                dl.remove(0)
                                dl.append(0)
                        except:pass
                        if mid == dl:
                                break
                return self.sumSameNum(dl)

        def handleData(self):
                lastdata=self.data.copy()
                m,n = self.data.shape
                for i in xrange(m):
                        newdi = self.removeZero(list(self.data[i]))
                        self.data[i] = newdi
                        for k in range(self.SIZE-1,self.SIZE-newdi.count(0)-1,-1):
                                self.zerolist.append((i,k))
                if self.data.min() == 0 and (lastdata != self.data).any():
                        self.data=otherTool().initData(self.SIZE,self.data,self.zerolist)

        def toNormalization(self):
                pass

        def getNext(self,SIZE,scorenow=0):
                self.SIZE = SIZE
                return self.toNormalization().copy(),self.score
                
                
class UpAction(NumUpdata):
        """docstring for UpAction"""
        def __init__(self, data):
                super(UpAction, self).__init__(data)

        def toNormalization(self):
                self.data = self.data.T
                self.handleData()
                return self.data.T


class DownAction(NumUpdata):
        """docstring for DownAction"""
        def __init__(self, data):
                super(DownAction, self).__init__(data)

        def toNormalization(self):
                self.data=self.data[::-1].T
                self.handleData()
                return self.data.T[::-1]


class LeftAction(NumUpdata):
        """docstring for LeftAction"""
        def __init__(self, data):
                super(LeftAction, self).__init__(data)

        def toNormalization(self):
                self.handleData()
                return self.data


class RightAction(NumUpdata):
        """docstring for RightAction"""
        def __init__(self, data):
                super(RightAction, self).__init__(data)

        def toNormalization(self):
                self.data = self.data[:,::-1]
                self.handleData()
                return self.data[:,::-1]

                
class KeyDownFactory(object):
        def getNext(self,SIZE,scorenow):
                return otherTool().initData(SIZE),-scorenow
        def factory(slef,kp,data):
                if kp[K_w]:
                        return UpAction(data),True
                elif kp[K_a]:
                        return LeftAction(data),True
                elif kp[K_s]:
                        return DownAction(data),True
                elif kp[K_d]:
                        return RightAction(data),True
                elif kp[K_SPACE]:
                        return KeyDownFactory(),True
                else:
                        return False,True


class MouseDownFactory(object):
        pass


class otherTool(object):
        def getInitRandomLocal(self,SIZE):
                a = random.randint(0,SIZE-1)
                b = random.randint(0,SIZE-1)
                return a,b
        
        def getNewNum(self):
                k = random.random()
                if k>0.95:n=4
                else:n=2
                return n
        
        def getNextRandomLocal(self, zl):
                return random.sample(zl, 1)[0]

        def initData(self,SIZE,data = None,zl = None):
                if data == None:data = DATA.copy()
                else:data = data.copy()
                if zl == None:a,b = self.getInitRandomLocal(SIZE)
                else:a,b = self.getNextRandomLocal(zl)
                n = self.getNewNum()
                data[a][b] = n
                return data

        def isEnd(self,data,SIZE):
                d0 = data.copy()
                d1 = UpAction(data.copy()).getNext(SIZE)[0]
                if (d0 != d1).any():return False
                d2 = DownAction(data.copy()).getNext(SIZE)[0]
                if (d0 != d2).any():return False
                d3 = LeftAction(data.copy()).getNext(SIZE)[0]
                if (d0 != d3).any():return False
                d4 = RightAction(data.copy()).getNext(SIZE)[0]
                if (d0 != d4).any():return False
                return True

        def drawSerface(self,screen,TITLE_RECT,scorenow,data,NUM_BLOCK,BLOCK_SPACE,BLOCK_COLOR):
                screen.fill((0,0,0))
                pygame.draw.rect(screen,(255,255,255),TITLE_RECT)
                font1 = pygame.font.SysFont("stxingkai", 40)
                font2 = pygame.font.SysFont("stxingkai", 20)
                screen.blit(font1.render("2048", True, (0, 0, 0)), (0, 0))
                screen.blit(font2.render(u"←:a  ↓:s  →:d     复位:空格", True, (0, 0, 0)), (250, 25))
                screen.blit(font2.render(u"↑:w", True, (0, 0, 0)), (294, 0))
                screen.blit(font1.render("SCORE:", True, (0, 0, 0)), (50, 50))
                screen.blit(font1.render(str(int(scorenow)), True, (0, 0, 0)), (200, 50))
                a,b = data.shape
                for i in xrange(a):
                        for k in xrange(b):
                                self.drawBlock(i,k,NUM_BLOCK,BLOCK_SPACE,BLOCK_COLOR[data[i][k]],screen,data[i][k])

        def drawBlock(slef,a,b,NUM_BLOCK,BLOCK_SPACE,color,screen,num):
                font = pygame.font.SysFont("stxingkai", 80)
                h = a*NUM_BLOCK+(a+1)*BLOCK_SPACE+110
                w = b*NUM_BLOCK+(b+1)*BLOCK_SPACE
                pygame.draw.rect(screen,color,(w,h,110,110))
                if num != 0:
                        f,t=font.size(str(int(num)))
                        screen.blit(font.render(str(int(num)), True, (0, 0, 0)), (w+(110-f)/2, h+(110-t)/2))


def main():
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
        data = otherTool().initData(SIZE)
        scorenow = SCORE 
        end = False 
        otherTool().drawSerface(screen,TITLE_RECT,scorenow,data,NUM_BLOCK,BLOCK_SPACE,BLOCK_COLOR)
        #print data
        #print scorenow
        while True:
                for event in pygame.event.get():
                        if event.type == QUIT:
                                exit()
                        elif event.type == KEYDOWN:
                                pressed_keys = pygame.key.get_pressed()
                                newdata , reset = KeyDownFactory().factory(pressed_keys,data)
                                if reset:end = False
                                if newdata and not end:
                                        data,score = newdata.getNext(SIZE,scorenow)
                                        scorenow += score
                                        if data.min() != 0:
                                                end = otherTool().isEnd(data,SIZE)
                                        otherTool().drawSerface(screen,TITLE_RECT,scorenow,data,NUM_BLOCK,BLOCK_SPACE,BLOCK_COLOR)
                                        #print data
                                        #print scorenow
                                        #print end
                pygame.display.update()


if __name__ == '__main__':
        main()
