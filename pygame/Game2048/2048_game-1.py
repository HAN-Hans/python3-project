import curses
from random import randrange, choice
# 使用dict时，如果引用的Key不存在，就会抛出KeyError。
# 如果希望key不存在时，返回一个默认值，就可以用defaultdict
from collections import defaultdict

#行为和有效输入
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']

# 将有效输入和行为进行关联，映射
actions_dict = dict(zip(letter_codes, actions * 2))

# 循环阻塞直到有效行为输入
def get_user_action(keyboard):
	char = 'N'
	while char not in actions_dict:
		char = keyboard.getch()
	return actions_dict[char]


# 下面两个对于提高代码重复率
# 矩阵转置
def transpose(field):
	return [list(row) for row in zip(*field)]
# 矩阵逆转
def invert(field):
	return [row[::-1] for row in field]

class GameField(object):
	"""docstring for GameField"""
	def __init__(self, height = 4, width = 4, win = 2048):
		super(GameField, self).__init__()
		self.height = height
		self.width = width
		self.win_value = win
		self.scroe = 0
		self.highscore = 0
		self.reset()

	def reset(self):
		if self.scroe > self.highscore:
			self.highscore = self.scroe
		self.scroe = 0
		# 初始化二维矩阵
		self.field = [[0 for i in range(self.width)] for j in range(self.height)]
		self.spawn()
		self.spawn()
	
	def is_win(self):
		return any(any(i >= self.win_value for i in row) for row in self.field)

	def is_gameover(self):
		return not any(self.move_is_possible(move) for move in actions)	

	# 随机向矩阵值为零的单元添加2或4
	def spawn(self):
		new_element = 4 if randrange(100) > 89 else 2
		(i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] ==0])
		self.field[i][j] = new_element

	# 根据不同的state绘制游戏界面
	def draw(self, screen):
		help_string1 = '(W)Up (S)Down (A)Left (D)Right'
		help_string2 = '     (R)Restart (Q)Exit'
		gameover_string = '           GAME OVER'
		win_string = '          YOU WIN!'

		def cast(string):
			screen.addstr(string + '\n')

		def draw_hor_separator():
			line = '+' + ('+------' * self.width + '+')[1:]
			separator = defaultdict(lambda: line)
			if not hasattr(draw_hor_separator, 'counter'):
				draw_hor_separator.counter = 0
			cast(separator[draw_hor_separator.counter])
			draw_hor_separator.counter += 1

		def draw_row(row):
			cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

		screen.clear()
		cast('SCORE: ' + str(self.scroe))
		if self.highscore != 0:
			cast('HIGHSCORE: ' + str(self.highscore))

		for row in self.field:
			draw_hor_separator()
			draw_row(row)

		draw_hor_separator()

		if self.is_win():
			cast(win_string)
		else:
			if self.is_gameover():
				print('123')
				cast(gameover_string)
			else:
				cast(help_string1)
		cast(help_string2)


	# 判断能否移动
	def move_is_possible(self, direction):
		def row_is_left_moveble(row):
			def change(i):
				if row[i] == 0 and row[i + 1] !=0:  # 可以移动
					return True
				if row[i] != 0 and row[i + 1] == row[i]:    # 可以合并
					return True	
				return False
			return any(change(i) for i in range(len(row) - 1))

		check = {}
		check['Left'] = lambda field: any(row_is_left_moveble(row) for row in field)
		check['Right'] = lambda field: check['Left'](invert(field))
		check['Up'] = lambda field: check['Left'](transpose(field))
		check['Down'] = lambda field: check['Right'](transpose(field))

		if direction in check:
			return check[direction](self.field)
		else:
			return False

	# 响应输入，移动矩阵
	def move(self, direction):
		# 一行向左移动
		def move_row_left(row):
			# 将非零的单元向左移
			def tighten(row):
				new_row = [i for i in row if i != 0]
				new_row += [0 for i in range(len(row) - len(new_row))]
				return new_row
			# 向左合并左右相等的单元
			def merge(row):
				pair = False
				new_row = []
				for i in range(len(row)):
					if pair:
						new_row.append(2 * row[i])
						self.scroe += 2 * row[i]
						pair = False
					else:
						if i + 1 < len(row) and row[i] == row[i + 1]:
							pair = True
							new_row.append(0)
						else:
							new_row.append(row[i])

				assert len(new_row) == len(row)
				return new_row
			# 先向左挤到一块再向右合并最后再挤到左侧
			return tighten(merge(tighten(row)))

		moves = {}
		moves['Left'] = lambda field: [move_row_left(row) for row in field]
		moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
		moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
		moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

		if direction in moves:
			if self.move_is_possible(direction):
				self.field = moves[direction](self.field)
				self.spawn()
				return True
			else:
				return False


def main(stdscr):

	def init():
		game_field.reset()
		return 'Game'

	def not_game(state):
		game_field.draw(stdscr)
		action = get_user_action(stdscr)
		responses = defaultdict(lambda: state)
		responses['Restart'], responses['Exit'] = 'Init', 'Exit'
		return responses[action]

	def game():
		game_field.draw(stdscr)
		action = get_user_action(stdscr)
		
		if action == 'Restart':
			return 'Init'
		if action == 'Exit':
			return 'Exit'
	
		if game_field.move(action):
			if game_field.is_win():
				return 'Win'
			if game_field.is_gameover():
				return 'Gameover'
		return 'Game'

	curses.use_default_colors()
	game_field = GameField(win = 2048)

	state_actions = {
	'Init': init,
	'Win': lambda: not_game('Win'),
	'Gameover': lambda: not_game('Gameover'),
	'Game': game
	}
	state = 'Init'

	while state != 'Exit':
		state = state_actions[state]()


if __name__ == '__main__':
	curses.wrapper(main)

