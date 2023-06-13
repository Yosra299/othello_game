from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy


nodes = 0
depth = 4
moves = 0

root = Tk()
screen = Canvas(root, width=500, height=600, background="#222",highlightthickness=0)
screen.pack()

class Board:
	def __init__(self):
		self.player = 0
		self.passed = False
		self.won = False
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append(None)

		self.array[3][3]="w"
		self.array[3][4]="b"
		self.array[4][3]="b"
		self.array[4][4]="w"

		self.oldarray = self.array
	def update(self):
		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):
				if self.oldarray[x][y]=="w":
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

				elif self.oldarray[x][y]=="b":
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		screen.update()
		for x in range(8):
			for y in range(8):
				if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="w":
					screen.delete("{0}-{1}".format(x,y))
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
					screen.update()

				elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]=="b":
					screen.delete("{0}-{1}".format(x,y))
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						screen.update()
						screen.delete("animated")

					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
					screen.update()

		for x in range(8):
			for y in range(8):
				if self.player == 0:
					if valid(self.array,self.player,x,y):
						screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#008000",outline="#008000")

		if not self.won:
			self.drawScoreBoard()
			screen.update()
			if self.player==1:
				startTime = time()
				self.oldarray = self.array
				alphaBetaResult = self.alphaBeta(self.array,depth,-float("inf"),float("inf"),1)
				self.array = alphaBetaResult[1]

				if len(alphaBetaResult)==3:
					position = alphaBetaResult[2]
					self.oldarray[position[0]][position[1]]="b"

				self.player = 1-self.player
				deltaTime = round((time()-startTime)*100)/100
				if deltaTime<2:
					sleep(2-deltaTime)
				nodes = 0
				self.passTest()
		else:
			screen.create_text(250,550,anchor="c",font=("Consolas",15), text="The game is done!")

	def boardMove(self,x,y):
		global nodes
		self.oldarray = self.array
		self.oldarray[x][y]="w"
		self.array = move(self.array,x,y)

		self.player = 1-self.player
		self.update()

		self.passTest()
		self.update()

	def drawScoreBoard(self):
		global moves
		screen.delete("score")

		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.array[x][y]=="w":
					player_score+=1
				elif self.array[x][y]=="b":
					computer_score+=1

		if self.player==0:
			player_colour = "green"
			computer_colour = "gray"
		else:
			player_colour = "gray"
			computer_colour = "green"

		screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
		screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)

		screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
		screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

		moves = player_score+computer_score

	def passTest(self):
		mustPass = True
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					mustPass=False
		if mustPass:
			self.player = 1-self.player
			if self.passed==True:
				self.won = True
			else:
				self.passed = True
			self.update()
		else:
			self.passed = False

	def dumbMove(self):
		choices = []
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					choices.append([x,y])
		dumbChoice = choice(choices)
		self.arrayMove(dumbChoice[0],dumbChoice[1])

	def slightlyLessDumbMove(self):
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		bestScore = -float("inf")
		bestIndex = 0
		for i in range(len(boards)):
			score= dumbScore(boards[i],self.player)
			if score>bestScore:
				bestIndex=i
				bestScore = score
		self.arrayMove(choices[bestIndex][0],choices[bestIndex][1])

	def decentMove(self):
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(self.array,x,y)
					boards.append(test)
					choices.append([x,y])

		bestScore = -float("inf")
		bestIndex = 0
		for i in range(len(boards)):
			score= slightlyLessDumbScore(boards[i],self.player)
			if score>bestScore:
				bestIndex=i
				bestScore = score
		self.arrayMove(choices[bestIndex][0],choices[bestIndex][1])

	def minimax(self, node, depth, maximizing):
		global nodes
		nodes += 1
		boards = []
		choices = []

		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([decentHeuristic(node,1-maximizing),node])

		if maximizing:
			bestValue = -float("inf")
			bestBoard = []
			for board in boards:
				val = self.minimax(board,depth-1,0)[0]
				if val>bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

		else:
			bestValue = float("inf")
			bestBoard = []
			for board in boards:
				val = self.minimax(board,depth-1,1)[0]
				if val<bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

	def alphaBeta(self,node,depth,alpha,beta,maximizing):
		global nodes
		nodes += 1
		boards = []
		choices = []

		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([finalHeuristic(node,maximizing),node])

		if maximizing:
			v = -float("inf")
			bestBoard = []
			bestChoice = []
			for board in boards:
				boardValue = self.alphaBeta(board,depth-1,alpha,beta,0)[0]
				if boardValue>v:
					v = boardValue
					bestBoard = board
					bestChoice = choices[boards.index(board)]
				alpha = max(alpha,v)
				if beta <= alpha:
					break
			return([v,bestBoard,bestChoice])
		else:
			v = float("inf")
			bestBoard = []
			bestChoice = []
			for board in boards:
				boardValue = self.alphaBeta(board,depth-1,alpha,beta,1)[0]
				if boardValue<v:
					v = boardValue
					bestBoard = board
					bestChoice = choices[boards.index(board)]
				beta = min(beta,v)
				if beta<=alpha:
					break
			return([v,bestBoard,bestChoice])

def move(passedArray,x,y):
	array = deepcopy(passedArray)
	if board.player==0:
		colour = "w"

	else:
		colour="b"
	array[x][y]=colour

	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!=None:
				neighbours.append([i,j])

	convert = []

	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]
		if array[neighX][neighY]!=colour:
			path = []

			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				if value==None:
					break
				if value==colour:
					for node in path:
						convert.append(node)
					break
				tempX+=deltaX
				tempY+=deltaY

	for node in convert:
		array[node[0]][node[1]]=colour

	return array

def drawGridBackground(outline=False):
	if outline:
		screen.create_rectangle(50,50,450,450,outline="#111")

	for i in range(7):
		lineShift = 50+50*(i+1)

		screen.create_line(50,lineShift,450,lineShift,fill="#111")

		screen.create_line(lineShift,50,lineShift,450,fill="#111")

	screen.update()

def dumbScore(array,player):
	score = 0
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	for x in range(8):
		for y in range(8):
			if array[x][y]==colour:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score

def slightlyLessDumbScore(array,player):
	score = 0
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	for x in range(8):
		for y in range(8):
			add = 1
			if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=3
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 5
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

def decentHeuristic(array,player):
	score = 0
	cornerVal = 25
	adjacentVal = 5
	sideVal = 5
	if player==1:
		colour="b"
		opponent="w"
	else:
		colour = "w"
		opponent = "b"
	for x in range(8):
		for y in range(8):
			add = 1

			if (x==0 and y==1) or (x==1 and 0<=y<=1):
				if array[0][0]==colour:
					add = sideVal
				else:
					add = -adjacentVal


			elif (x==0 and y==6) or (x==1 and 6<=y<=7):
				if array[7][0]==colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x==7 and y==1) or (x==6 and 0<=y<=1):
				if array[0][7]==colour:
					add = sideVal
				else:
					add = -adjacentVal

			elif (x==7 and y==6) or (x==6 and 6<=y<=7):
				if array[7][7]==colour:
					add = sideVal
				else:
					add = -adjacentVal


			elif (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=sideVal
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = cornerVal
			if array[x][y]==colour:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

def finalHeuristic(array,player):
	if moves<=8:
		numMoves = 0
		for x in range(8):
			for y in range(8):
				if valid(array,player,x,y):
					numMoves += 1
		return numMoves+decentHeuristic(array,player)
	elif moves<=52:
		return decentHeuristic(array,player)
	elif moves<=58:
		return slightlyLessDumbScore(array,player)
	else:
		return dumbScore(array,player)

def valid(array,player,x,y):
	if player==0:
		colour="w"
	else:
		colour="b"

	if array[x][y]!=None:
		return False

	else:
		neighbour = False
		neighbours = []
		for i in range(max(0,x-1),min(x+2,8)):
			for j in range(max(0,y-1),min(y+2,8)):
				if array[i][j]!=None:
					neighbour=True
					neighbours.append([i,j])
		if not neighbour:
			return False
		else:
			valid = False
			for neighbour in neighbours:

				neighX = neighbour[0]
				neighY = neighbour[1]

				if array[neighX][neighY]==colour:
					continue
				else:
					deltaX = neighX-x
					deltaY = neighY-y
					tempX = neighX
					tempY = neighY

					while 0<=tempX<=7 and 0<=tempY<=7:
						if array[tempX][tempY]==None:
							break
						if array[tempX][tempY]==colour:
							valid=True
							break
						tempX+=deltaX
						tempY+=deltaY
			return valid

def clickHandle(event):
	global depth
	xMouse = event.x
	yMouse = event.y
	if running:
		if xMouse>=450 and yMouse<=50:
			root.destroy()
		elif xMouse<=50 and yMouse<=50:
			playGame()
		else:
			if board.player==0:
				x = int((event.x-50)/50)
				y = int((event.y-50)/50)
				if 0<=x<=7 and 0<=y<=7:
					if valid(board.array,board.player,x,y):
						board.boardMove(x,y)
	else:
		if 300<=yMouse<=350:
			if 25<=xMouse<=155:
				depth = 1
				playGame()
			elif 180<=xMouse<=310:
				depth = 4
				playGame()
			elif 335<=xMouse<=465:
				depth = 6
				playGame()

def keyHandle(event):
	symbol = event.keysym
	if symbol.lower()=="r":
		playGame()
	elif symbol.lower()=="q":
		root.destroy()

def create_buttons():
		screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
		screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

		screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
		screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

		screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
		screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")

		screen.create_line(455,5,495,45,fill="white",width="3")
		screen.create_line(495,5,455,45,fill="white",width="3")

def runGame():
	global running
	running = False
	screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
	screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")

	screen.create_text(250,270,anchor="c",text="Choose Difficulty",font=("Consolas", 30),fill="#aaa")

	for i in range(3):
		screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
		screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

		spacing = 130/(i+2)
		for x in range(i+1):
			screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="*", font=("Consolas", 25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="*", font=("Consolas",25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="*", font=("Consolas", 25),fill="#ffd700")

	screen.update()

def playGame():
	global board, running
	running = True
	screen.delete(ALL)
	create_buttons()
	board = 0

	drawGridBackground()

	board = Board()
	board.update()

runGame()

screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

root.wm_title("Othello")
root.mainloop()
