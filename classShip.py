from random import randint
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Dot:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __repr__(self):
		return f"Dot({self.x},{self.y})"

class Ship:

	def __init__(self, length, dot, direction):
		self.length = length
		self.dot = dot
		self.direction = direction
		self.life = length
		self.areaa = []
	@property
	def dots(self):
		L = []
		if self.direction == 0:
			for i in range(1, self.length + 1):
				L.append((self.dot.x, self.dot.y + i - 1))
			return L
		elif self.direction == 1:
			for i in range(1, self.length + 1):
				L.append((self.dot.x + i - 1, self.dot.y))
			return L

class Board:
	def __init__(self, hid = True):
		self.list_board = [["O"]*6 for _ in range(6)]
		self.list_ships = []
		self.ships = []
		self.hid = hid
		self.living_ships = 0
		self.area = []

	@property
	def print_board(self):
		if self.hid:
			print(" | 1 | 2 | 3 | 4 | 5 | 6 |")
			for i in range(1, 7):
				print(f"{i}|", " | ".join(self.list_board[i-1]), "|")
		else:
			print(" | 1 | 2 | 3 | 4 | 5 | 6 |")
			for i in range(1, 7):
				print(f"{i}|", (" | ".join(self.list_board[i - 1])).replace("■", "O"), "|")
		print("-------------------------")

	def add_ship(self, sh):
			K = sh.dots
			count_dot = 0
			for (i,j) in sh.dots:
				if (i,j) in self.area or not self.out(Dot(i,j)) or (i, j) in self.list_ships:
					raise BoardWrongShipException()
			for i, j in K:
				if self.out(Dot(i,j)) and self.list_board[i-1][j-1] == 'O':
					count_dot +=1
			for i, j in K:
				if count_dot == len(K):
					self.list_board[i-1][j-1] = "■"
					self.list_ships += [(i,j)]
			if count_dot == len(K):
				self.ships.append(sh)
				return True

	def add_area(self, sh):
		for (i, j) in sh.areaa:
			self.list_board[i-1][j-1] = "T"
			self.area += [(i, j)]


	def out(self, Dot):
			return 0 < Dot.x < 7 and 0 < Dot.y < 7

	def contour(self,sh):
		L = []
		K = sh.dots
		if self.add_ship(sh):
			for i, j in K:
						L.append(Dot(i - 1, j - 1))
						L.append(Dot(i - 1, j))
						L.append(Dot(i - 1, j+1))
						L.append(Dot(i, j-1))
						L.append(Dot(i, j))
						L.append(Dot(i, j+1))
						L.append(Dot(i+1, j - 1))
						L.append(Dot(i+1, j))
						L.append(Dot(i+1, j + 1))
			N = [(a.x, a.y) for a in L if self.out(a)]
			M = list(set(N).difference(set(K)))
			sh.areaa = M
			self.area += M
			self.living_ships += 1
			return M
	def shot(self,dott):
		if not self.out(dott):
			raise BoardOutException()
		if (dott.x, dott.y) in self.area:
			raise BoardUsedException()

		for i in self.ships:
			if (dott.x, dott.y) in i.dots:
				i.life -= 1
				self.list_board[dott.x - 1][dott.y - 1] = 'X'
				self.area.append((dott.x, dott.y))
				if i.life == 0:
					self.living_ships -= 1
					self.add_area(i)
					print("КОРАБЛЬ УНИЧТОЖЕН")
				return True
		for i in self.ships:
			if (dott.x, dott.y) not in i.dots and self.list_board[dott.x - 1][dott.y - 1] != 'T':
				self.list_board[dott.x - 1][dott.y - 1] = '.'
				self.area.append((dott.x, dott.y))
				return False

class Player:
	def __init__(self, my, comp):
		self.my = my
		self.comp = comp
	def ask(self):
		raise NotImplementedError()
	def move(self):
		while True:
			try:
				coordinate_set = self.ask()
				repeat = self.comp.shot(coordinate_set)
				return repeat
			except BoardException as x:
				print(x)
class AI(Player):
	def ask(self):
		Z = Dot(randint(0,5),randint(0,5))
		print(f'Ход компьютера: {Z.x}, {Z.y}')
		return Z
class User(Player):
	def ask(self):
		while True:
			c = input("Ваш ход: ").split()
			if len(c) != 2:
				print("Введите 2 числа! ")
				continue
			x, y = c
			if not (x.isdigit()) or not (y.isdigit()):
				print("Введите числа! ")
				continue
			x, y = int(x), int(y)
			return Dot(x, y)
class Game:
	def __init__(self):
		pl = self.random_board()
		co = self.random_board()
		co.hid = False
		self.ai = AI(co, pl)
		self.us = User(pl, co)

	def random_board(self):
		B = None
		while B is None:
			B = self.random()
		return B


	def random(self):
		len_ships = [3,2,2,1,1,1,1]
		B = Board()
		count = 0
		for i in len_ships:
			while True:
				count += 1
				if count > 2000:
					return None
				try:
					B.contour(Ship(i, Dot(randint(0, 6), randint(0, 6)), randint(0, 1)))
					break
				except BoardWrongShipException:
					pass
		B.area =[]
		return B

	def greet(self):
		print("-------ИГРА МОРСКОЙ БОЙ-------")
		print("------------------------------")
		print("-формат ввода: координаты x y-")
		print("------------------------------")

	def loop(self):
		num = 0
		while True:
			print("Доска пользователя:")
			(self.us.my).print_board
			print("Доска компьютера:")
			(self.ai.my).print_board
			if num % 2 == 0:
				print("Ходит пользователь!")
				repeat = self.us.move()
			else:
				print("Ходит компьютер!")
				repeat = self.ai.move()
			if repeat:
				num -= 1
			if self.ai.my.living_ships == 0:
				print("Пользователь выиграл!")
				break
			if self.us.my.living_ships == 0:
				print("Компьютер выиграл!")
				break
			num += 1
	def start(self):
		self.greet()
		self.loop()

V = Game()
V.start()

