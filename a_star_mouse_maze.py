import numpy as np
import copy
import heapq

class cell:
	hex_to_bin =  {
		'0': "0000",'1': "0001",'2': "0010",'3': "0011",
		'4': "0100",'5': "0101",'6': "0110",'7': "0111",
		'8': "1000",'9': "1001",'a': "1010",'b': "1011",
		'c': "1100",'d': "1101",'e': "1110",'f': "1111"
	}

	def __init__(self, s, m):
		self.c = self.hex_to_bin[s]
		self.s = s
		self.m = 1 if m == True else 0

	def flip_mouse(self):
		if self.m == 1:
			self.m = 0	
		else:
			self.m = 1	

	def cell_h_string(self):
		w = '#'
		b = ' '
		x = 'X'
		v = '|'
		h = '-'
		if self.m == 1:
			cell_string = [[w,h,w],[v,x,v],[w,h,w]]
		else:
			cell_string = [[w,h,w],[v,b,v],[w,h,w]]	
		if self.c[3] == '1':
			cell_string[1][0] = b
		if self.c[2] == '1':
			cell_string[2][1] = b
		if self.c[1] == '1':
			cell_string[1][2] = b
		if self.c[0] == '1':
			cell_string[0][1] = b
		return cell_string

	def r_string(self,i):
		row_string = ""
		for j in range(3):
			row_string += self.cell_h_string()[i][j]
		return row_string

	def cell_string(self):
		string = ""
		for i in range(3):
			string += self.r_string(i)
			string += '\n'
		return string
			
	def hor_adj(self, cell):
		return self.c[1] == '1' and cell.c[3] == '1'

	def ver_adj(self, cell):
		return self.c[2] == '1' and cell.c[0] == '1'

class maze:
	def __init__(self, n, m, s, mouse, fast= True):
		self.n = n
		self.m = m
		self.g = 0
		self.s = s
		self.cells = []
		self.mouse = mouse
		for i in range(n):
			new_row = []
			for j in range(m):
				c = cell(s[i*n+j], (i,j)==mouse)
				new_row.append(c)	
			self.cells.append(new_row)	
		self.adj_gra = np.zeros((n*m,m*m))
		if fast == False:
			self.update_graph()
		self.reachable = set()
		if fast == False:
			self.update_reachable()

	def update_graph(self):
		n = self.n
		m = self.m
		self.adj_gra = np.zeros((n*m,m*m))
		for i in range(n-1):
			for j in range(m-1):
				if self.cells[i][j].hor_adj(self.cells[i][j+1]):
					self.adj_gra[i*m+j][i*m+j+1] = 1
					self.adj_gra[i*m+j+1][i*m+j] = 1
				if self.cells[i][j].ver_adj(self.cells[i+1][j]):
					self.adj_gra[i*m+j][i*m+j+m] = 1
					self.adj_gra[i*m+j+m][i*m+j] = 1
		for i in range(1,n):
			for j in range(1,m):
				if self.cells[i][j-1].hor_adj(self.cells[i][j]):
					self.adj_gra[i*m+j][i*m+j-1] = 1
					self.adj_gra[i*m+j-1][i*m+j] = 1
				if self.cells[i-1][j].ver_adj(self.cells[i][j]):
					self.adj_gra[i*m+j][i*m+j-m] = 1
					self.adj_gra[i*m+j-m][i*m+j] = 1

	def slide_row(self,i):
		new_head = self.cells[i][self.m-1]
		new_buffer = self.cells[i][0] 
		self.cells[i][self.m-1] = self.cells[i][self.m-2]
		for j in range(self.m-1):
			self.cells[i][j] = new_head
			new_head = new_buffer
			new_buffer = self.cells[i][j+1] 
		if self.mouse[0] == i:
			self.mouse = (self.mouse[0],(self.mouse[1]+1)%self.m)
		self.update_reachable()

	def slide_col(self,j):
		new_head = self.cells[self.n-1][j]
		new_buffer = self.cells[0][j] 
		self.cells[self.n-1][j] = self.cells[self.n-2][j]
		for i in range(self.n-1):
			self.cells[i][j] = new_head
			new_head = new_buffer
			new_buffer = self.cells[i+1][j] 
		if self.mouse[1] == j:
			self.mouse = ((self.mouse[0]+1)%self.n,self.mouse[1])
		self.update_reachable()

	def move_mouse(self, i,j):
		k  =  self.mouse[0]
		l  =  self.mouse[1]
		self.mouse = (i,j)
		self.cells[i][j].flip_mouse() 
		self.cells[k][l].flip_mouse() 
		self.update_reachable()

	def update_reachable(self):
		self.update_graph()
		self.update_s()
		self.reachable = set()
		i = self.mouse[0]
		j = self.mouse[1]
		n = self.n
		m = self.m
		walks = copy.deepcopy(self.adj_gra)
		for t in range(n+m):
			for a in range(n):
				for b in range(m):
					if walks[i*n+j][a*n+b] >0:
						self.reachable.add((a,b))
			walks = np.matmul(walks,self.adj_gra)
		if (i,j) in self.reachable:
			self.reachable.remove((i,j))
				
	def legal_move(self, s, t):
		if len(s) != 2:
			return False
		elif s[0] == 'r' or s[0] == 'R':
			if int(s[1]) < self.n and t%2 == 1: 
				return True	
			else:
				return False
		elif s[0] == 'c' or s[0] == 'C':
			if int(s[1]) < self.m and t%2 == 1: 
				return True	
			else:
				return False
		elif (int(s[0]), int(s[1])) in self.reachable:
			if t%2 == 0: 
				return True	
			else:
				return False
		else:
			return False

	def play(self, s):
		if s[0] == 'r' or s[0] == 'R':
			self.slide_row(int(s[1]))
		elif s[0] == 'c' or s[0] == 'C':
			self.slide_col(int(s[1]))
		else:
			self.move_mouse(int(s[0]), int(s[1]))
	
	def update_s(self):
		string = ""
		for i in range(n):
			for j in range(m):
				string += self.cells[i][j].s
		self.s = string

	def slide_heuristic(self):
		a,b = self.mouse[0], self.mouse[1]
		n,m = self.n, self.m 
		max_white_space = 0
		for i in range(a,n):
			for j in range(b,m):
				count = 0
				for k in range(i,n):
					for l in range(j,m):
						if self.adj_gra[i*m+j][k*m+l] >= 0:
							count += 1
				if count > max_white_space: 
					max_white_space = count	
		return min(n+m, max_white_space)

	def move_heuristic(self):
		a,b = self.mouse[0], self.mouse[1]
		return a+b

	def heuristic(self):
		n,m = self.n, self.m 
		return max(n+m - self.move_heuristic() - self.slide_heuristic(), 0)

	def heuristic_at(self, x, y):
		n,m = self.n, self.m 
		return max(n+m - x+y - self.slide_heuristic(), 0)
			
	def maze_string(self):
		string = ""
		for row in self.cells:
			for i in range(3):
				row_string = ""
				for cell in row:
					row_string += cell.r_string(i)
				row_string += '\n'
				string += row_string
		return string		

class tree:
	def __init__(self, n, m, start, max_depth):
		self.explored = set()
		self.frontier_paths = []
		heapq.heapify(self.frontier_paths)
		self.col_moves = ['c'+x for x in [str(y) for y in range(m)]]		
		self.row_moves = ['r'+x for x in [str(y) for y in range(n)]]		
		self.max_depth = max_depth
		self.n = n 
		self.m = m
		self.search(maze(n,m,start,(0,0)))

	def expand_node(self, node, path):
		old = (node.s, node.mouse)
		self.explored.add(old)
		if node.mouse == (n-1,m-1):
			f = open("moves.txt", "a")
			f.write(str(path)+'\n')
			f.close()
			return True
		if len(path) >= self.max_depth:
			return
		if len(path)%2 == 0:
			node.update_reachable()
			for move in node.reachable:
				new = (node.s,(int(move[0]),int(move[1])))
				if not new in self.explored:
					new_path = list(path)
					new_path.append((int(move[0]),int(move[1])))
					distance = node.heuristic_at(int(move[0]),int(move[1]))
					heapq.heappush(self.frontier_paths,(distance,new,tuple(new_path)))
		else:
			for move in self.col_moves:
				new_node = maze(node.n, node.m, node.s, node.mouse) 
				new_node.slide_col(int(move[1]))
				new = (new_node.s, new_node.mouse)
				if not new in self.explored:
					new_path = list(path)
					new_path.append(move)
					distance = new_node.heuristic()
					heapq.heappush(self.frontier_paths,(distance,new,tuple(new_path)))
			for move in self.row_moves:
				new_node = maze(node.n, node.m, node.s, node.mouse) 
				new_node.slide_row(int(move[1]))
				new = (new_node.s, new_node.mouse)
				if not new in self.explored:
					new_path = list(path)
					new_path.append(move)
					distance = new_node.heuristic()
					heapq.heappush(self.frontier_paths,(distance,new,tuple(new_path)))

	def search(self, start):
		self.expand_node(start,()) 
		while self.frontier_paths:
			d, p, path = heapq.heappop(self.frontier_paths)
			if self.expand_node(maze(self.n, self.m, p[0], p[1]), path) == True:
				return
					
					
print("Welcome to mouse maze")
print("Would you like to play the 7-game or the 10-game")
game_size = int(input())
if game_size == 7 :
	n = 7
	m = 7
	number_of_moves = 6
	s  = "65dd9ac3e53d7aaa7aac39ea399a57cc6aa9393ac5399399a"
	t = tree(n,m,s,number_of_moves)
elif game_size == 10:
	n = 10 
	m = 10
	number_of_moves = 14
	s  = "7e3593b53ec55e9e7a6ec759e9a66cb35ea9639c753c356633599336a5a97599556a9c6aa553cc6355a3da56aa693aaae3c9"
	t = tree(n,m,s,number_of_moves)
else:
	print("Invalid Game Size")
	exit()

