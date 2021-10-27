
		strin = ""
		for i in range(3):
			row_string = ""
			for cell in self.cells[i]:
				row_string += cell.r_string(i)
			row_string += '\n'
			strin += row_string 
		print(strin)	















		new_row = []
		new_row.append(self.cells[i][self.m-1])
		print("new_row")
		print(new_row[0].cell_string())
		for j in range(1,self.m):
			new_row.append(self.cells[i][j])
			print(new_row[j].cell_string())
		print("new_row")
		for j in range(self.m):
			print(new_row[j].cell_string())
			self.cells[i][j] = new_row[j]	
		self.move_mouse(self.mouse[0],(self.mouse[1]+1)%self.m)
		self.update_graph()
		self.update_reachable()
