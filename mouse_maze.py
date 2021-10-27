import numpy as np
import copy

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

	def cell_string(self):
		w = '#'
		x = 'X'
		b = ' '
		if self.m == 1:
			cell_string = [[w,w,w],[w,x,w],[w,w,w]]
		else:
			cell_string = [[w,w,w],[w,b,w],[w,w,w]]	
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
			row_string += self.cell_string()[i][j]
		return row_string

	def hor_adj(self, cell):
		return self.c[1] == '1' and cell.c[3] == '1'

	def ver_adj(self, cell):
		return self.c[2] == '1' and cell.c[0] == '1'

class maze:
	cells   = []

	def __init__(self, n, m, s, mouse):
		self.n = n
		self.m = m
		self.g = 0
		self.s = s
		self.mouse = mouse
		for i in range(n):
			new_row = []
			for j in range(m):
				c = cell(s[i*n+j], (i,j)==mouse)
				new_row.append(c)	
			self.cells.append(new_row)	
		self.adj_gra = np.zeros((n*m,m*m))
		self.update_graph()
		self.reachable = set()
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

	def slide_row(self,i):
		new_row = []
		new_row.append(self.cells[i][self.m-1])
		for j in range(1,self.m):
			new_row.append(self.cells[i][j])
		self.cells[i] = new_row	
		self.move_mouse(self.mouse[0],(self.mouse[1]+1)%self.m)
		self.update_graph()
		self.update_reachable()

	def slide_col(self,j):
		new_col = []
		new_col.append(self.cells[self.m-1][j])
		for i in range(1,self.n):
			new_col.append(self.cells[i][j])
		for i in range(self.n):
			self.cells[i][j] = new_col[i]
		self.move_mouse((self.mouse[0]+1)%self.n,self.mouse[1])
		self.update_graph()
		self.update_reachable()

	def move_mouse(self, i,j):
		k  =  self.mouse[0]
		l  =  self.mouse[1]
		self.mouse = (i,j)
		c1 = cell(self.s[i*self.n+j], (i,j)==self.mouse)
		c2 = cell(self.s[k*self.n+l], (k,l)==self.mouse)
		self.cells[i][j] = c1	
		self.cells[k][l] = c2	
		self.update_graph()
		self.update_reachable()

	def update_reachable(self):
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
						
					
n = 4
m = n
#s  = "9182df2ec797b9c88df0af877be505daa6f6575a3cf4c5623"
#s  = "9afde5e326d7e2dd"
#s  = "65dd9ac3e53d7aaa7aac39ea399a57cc6aa9393ac5399399a"
s  = "65dd9ac3da7aac39a"
ma = maze(n,m,s,(0,0))
print(ma.reachable)
print(ma.maze_string())
print(ma.mouse)
print(ma.adj_gra)
ma.slide_row(0)
print(ma.reachable)
print(ma.maze_string())
print(ma.mouse)
print(ma.adj_gra)
ma.slide_row(0)
print(ma.reachable)
print(ma.maze_string())
print(ma.mouse)
print(ma.adj_gra)
ma.slide_col(1)
print(ma.reachable)
print(ma.maze_string())
print(ma.mouse)
print(ma.adj_gra)
ma.move_mouse(n-2,2)
print(ma.reachable)
print(ma.maze_string())
print(ma.mouse)
print(ma.adj_gra)

#for row in ma.cells:
#	for cell in row:
#		print(cell.c)
#		print(cell.cell_string())
#		for i in range(3):
#			print(cell.r_string(i))

