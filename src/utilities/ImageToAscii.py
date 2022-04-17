"""
@author: Max Marshall
@desc:
@created: 04/14/2022
"""
import os
import math
from re import L
import PIL.Image as Image

class ImageToAscii:
	def __init__(self, image_file):
		self.im_file = image_file
		self.ascii = None
		self.fslash = [[0,0,1],[0,1,0],[1,0,0]]
		self.bslash = [[1,0,0],[0,1,0],[0,0,1]]
		self.dash = [[0,0,0],[0.5,1,0.5],[0,0,0]]
		self.under = [[0,0,0],[0,0,0],[1,1,1]]
		self.lbrack = [[1,1,0],[1,0,0],[1,1,1]]
		self.rbrack = [[0,1,1],[0,0,1],[0,1,1]]
		self.t = [[1,1,1],[0,1,0],[0,1,0]]
		self.plus = [[0,1,0],[1,1,1],[0,1,0]]
		self.space = [[0,0,0],[0,0,0],[0,0,0]]
		self.n = [[1,0,1],[1,1,1],[1,0,1]]
		self.z = [[1,1,1],[0,1,0],[1,1,1]]
		self.larrow = [[0,1,0],[1,0,0],[0,1,0]]
		self.rarrow = [[0,1,0],[0,0,1],[0,1,0]]
		self.chars = [self.fslash,self.bslash,self.dash,self.under,self.lbrack,self.rbrack,self.t,self.plus,self.space,self.n,self.z,self.larrow,self.rarrow]
		self.charvals = ["/","\\","-","_","[","]","T","+"," ","N","Z","<",">"]
		self.colors = ["\033[37m","\033[31m","\033[32m","\033[34m"]
	
	def open_image(self):
		self.im = Image.open(self.im_file)
		#self.im.show()
		self.x,self.y = self.im.size
		self.aspect_ratio = self.y/float(self.x)
		#print(self.aspect_ratio)
		#print(self.x,self.y)

	def get_chunk(self,i,j,i_max,j_max):
		# Returns top left and bottom right corners of box
		delta_i = self.x // (i_max)
		delta_j = self.y // (j_max)
		return delta_i*i, delta_j*j, delta_i*(i+1), delta_j*(j+1)

	def chunk_to_char(self, xmin, ymin, xmax, ymax):
		delta_x = (xmax-xmin) // 3
		delta_y = (ymax-ymin) // 3
		block = []
		maximum = [0,0,0,0]
		for x in range(3):
			row = []
			for y in range(3):
				row.append(self.avg_of_chunk(xmin+(delta_x*x),ymin+(delta_y*y),xmin+(delta_x*(x+1)),ymin+(delta_y*(y+1))))
				for z in range(4):
					if row[y][z] > maximum[z]:
						maximum[z] = row[y][z]
			block.append(row)
		max_z = 0
		z_index = 0
		for z in range(4):
			if maximum[z] > max_z:
				max_z = maximum[z]
				z_index = z
		for i in range(3):
			for j in range(3):
				if max_z > 0.0:
					block[i][j] = block[i][j][z_index]/float(max_z)
				else:
					block[i][j] = 0.0
		lowest_error = 1000000
		char_index = -1
		for i in range(len(self.chars)):
			error = 0
			for x in range(3):
				for y in range(3):
					error += abs(self.chars[i][x][y]-block[x][y])
			#print(error)
			if error < lowest_error:
				lowest_error = error
				char_index = i
		print(self.colors[z_index]+self.charvals[char_index],end="")
		#self.print_block(block,0)
		

	def avg_of_chunk(self,xmin,ymin,xmax,ymax):
		avg = [0.0, 0.0, 0.0, 0.0]
		for x in range(xmin,xmax):
			for y in range(ymin,ymax):
				value = self.im.getpixel((x,y))
				white = (value[0]+value[1]+value[2])/3.0
				avg[0] += white
				avg[1] += value[0]
				avg[2] += value[1]
				avg[3] += value[2]
		avg[0] = avg[0]/((xmax-xmin)*(ymax-ymin))
		avg[1] = avg[1]/((xmax-xmin)*(ymax-ymin))
		avg[2] = avg[2]/((xmax-xmin)*(ymax-ymin))
		avg[3] = avg[3]/((xmax-xmin)*(ymax-ymin))
		return avg

	def print_block(self, block, color):
		print("================")
		for row in block:
			for item in row:
				print("{:.2f}".format(item[color]),end="  ")
			print()
		print("================")

	def convert_to_ascii(self, num_cols, num_rows):
		print(self.aspect_ratio)
		print(num_cols*.5*self.aspect_ratio)
		map_scalar = math.floor(min([num_cols*.5*self.aspect_ratio, num_rows]))
		print(map_scalar)
		for j in range(map_scalar):
			for i in range(int(map_scalar*3.5)):
				xmin,ymin,xmax,ymax = self.get_chunk(i,j,int(map_scalar*3.5),map_scalar)
				self.chunk_to_char(xmin,ymin,xmax,ymax)
			print()
		print("\033[0m",end="")

# Testing
if __name__ == '__main__':
	class_test = ImageToAscii("../../data/map.jpg")
	class_test.open_image()
	class_test.convert_to_ascii(119,25)

