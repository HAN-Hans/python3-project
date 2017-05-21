1. 引言
     2048 这段时间火的不行啊，大家都纷纷仿造，“百家争鸣”，于是出现了各种技术版本：除了手机版本，还有C语言版、Qt版、Web版、java版、C#版等，刚好我接触Python不久，于是弄了个Python版——控制台的2048，正好熟悉下Python语法，程序运行效果如下：

图 1  Python版控制台2048运行截图

     程序代码加上注释大概150行左右，利用了一些Python内置数据类型的操作节省了不少代码量。下面说说我的编写思路，最后会给出源代码。

2. 2048 实现思路

     2.1 游戏规则
     这个游戏可玩性很好，简单的移动方向键让数字叠加，并且获得这些数字每次叠加后的得分，当出现2048这个数字时游戏胜利。同时每次移动方向键时，都会在这个4*4的方格矩阵的空白区域随机产生一个数字2或者4，如果方格被数字填满了，那么就GameOver了。
     

     2.2 实现思路
     这个游戏的全部操作都是围绕着一个4*4的矩阵进行，每次从用户界面获取用户的操作（即移动方向），然后重新计算这个4*4矩阵的状态，最后刷新用户界面显示4*4矩阵的最新状态，不断的循环这个过程，直到出现2048或没有空白方块了，下面是一个处理流程示意图：
     
     我写的是控制台程序，没有UI界面，因此用字符（W/S/A/D）代表方向键的输入，以数字0代表空白方格。接下来是计算部分，以向左移动为例，4*4矩阵在接收到向左移动的指令后，应该将每行的数字向左叠加， 将一行的叠加操作定义为函数 handle(list, direction)，其第一个参数用来存储4*4矩阵中的某一行（列），第二个参数表示移动的方向（上下左右）。

     这样当左右移动方向键时，可以这样来计算矩阵：遍历矩阵的每行，并将每行的数字沿左或右进行叠加操作。
for row in matrix:
         handle(row, direction)

     对于上下移动方向键时，由于矩阵是按行存储的，不能直接处理矩阵中的列，可以通过变通采用上面的函数handle()。对于矩阵中每一列，先将其拷贝到一个列表中，然后调用handle()函数对该列表进行叠加处理，最后再将叠加后的新列表拷贝回原始矩阵中其所在的列，其逻辑上等同于下面的代码操作。
for col in matrix:
          handle(col, direction)

     handle(row, direction)函数的作用是沿指定方向叠加一行中的数字，请看下面几个例子：
移动方向	移动前	移动后
handle(x, 'left')
x = [0, 2, 2, 2] 
x = [4, 2, 0, 0]
handle(x, 'left')	
x = [2, 4, 2, 2]
x = [2, 8, 0, 0]
handle(x, 'right')	x = [2, 4, 2, 2]	x = [0, 0, 2, 8]

实现 handle(row, direction) 函数

    根据上面的介绍，实现handle函数是关键。仔细观察叠加的过程，其都是由两个子过程组成的：
(1) align(row, direction)   沿direction方向对齐列表row中的数字，例如：
x = [0, 4, 0, 2]
align(x, 'left')  后 x = [4, 2, 0, 0]
在 align(x, 'right') 后 x = [0, 0, 4, 2]

(2) addSame(row, direction) 查找相同且相邻的数字。如果找到，将其中一个翻倍，另一个置0
（如果direction是'left'将左侧翻倍，右侧置0，如果direction为'right'，将右侧翻倍，左侧置0），
并返回True；否则，返回False。例如：
x = [2, 2, 2, 2]
addSame(x, 'left') 后 x = [4, 0, 2, 2]      返回 True
再 addSame(x, 'left') 后 x = [4, 0, 4, 0]   返回 True
再 addSame(x, 'left') 后 x = [4, 0, 4, 0]   返回 False 

     有了上面两个子函数，应该不难实现。有了这两个子函数，函数handle()就很好实现了，如下：
handle(row, direction):
          align(row, direction)
          result = addSame(row, direction)
          while result == True:
                    align(row, direction)
                    result = addSame(row, direction)

     下面结合一个实际例子再来看看handle函数的处理过程：
x = [2, 4, 2, 2]
调用 handle(x, 'right')，变量 x 变化过程：
align(x, 'right')          ->     [2, 4, 2, 2]
addSame(x, 'right')   ->     [2, 4, 0, 4]     ->     return True
align(x, 'right')          ->     [0, 2, 4, 4]    
addSame(x, 'right')   ->     [0, 2, 0, 8]     ->     return True
align(x, 'right')          ->     [0, 0, 2, 8]    
addSame(x, 'right')   ->     [0, 0, 2, 8]     ->     return False
最终得到的 x = [0, 0, 2, 8]
     
     最主要的部分已经说完了，下面就贴出代码吧，由于代码不多就直接贴出来吧。