import random

SIZE = 4
class Map(object):
    """docstring for Map"""
    def __init__(self, size = SIZE, win = 2048):
        super(Map, self).__init__()
        self.size = size
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.matrix = [[1, 1, 1, 2], [0, 1, 0, 1], [1, 0, 1, 0], [2, 1, 0, 1]]

    def add(self):
        new_element = 4 if random.randrange(100) > 85 else 2
        (i,j) = random.choice([(i,j) for i in range(self.size) for j in range(self.size) if self.matrix[i][j] ==0]) 
        self.matrix[i][j] = new_element
        
    def is_win(self):
        return any(any((i > self.win_value) for i in row) for row in self.matrix)

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
        print(self.matrix)

    def moveRight(self):
        self.invert()
        if self.move_is_possible():
            self.add()
        self.invert()
        print(self.matrix)        

    def moveUp(self):
        self.transpose()
        if self.move_is_possible():
            self.add()
        self.transpose()
        print(self.matrix)  

    def moveDown(self):
        self.transpose()
        self.invert()
        if self.move_is_possible():
            self.add()
        self.invert()
        self.transpose()
        print(self.matrix)

map = Map()
map.moveDown()