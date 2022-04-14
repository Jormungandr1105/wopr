"""
@author: Max Marshall
@desc:
@created: 04/14/2022
"""
import os
import math
import PIL.Image as Image

class ImageToAscii:
	def __init__(self, image_file):
		self.im_file = image_file
		self.ascii = None
	
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
		for x in range(3):
			row = []
			for y in range(3):
				row.append(self.avg_of_chunk(xmin+(delta_x*x),ymin+(delta_y*y),xmin+(delta_x*(x+1)),ymin+(delta_y*(y+1))))
			block.append(row)
		self.print_block(block,0)
		

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
		print("=============")
		for row in block:
			for item in row:
				print("{:3d}".format(int(item[color])),end=" ")
			print()
		print("=============")

	def convert_to_ascii(self, num_cols, num_rows):
		print(num_cols*.5*self.aspect_ratio)
		map_scalar = math.floor(min([num_cols*.5*self.aspect_ratio, num_rows])+.5)
		print(map_scalar)
		for j in range(map_scalar):
			for i in range(map_scalar*2):
				xmin,ymin,xmax,ymax = self.get_chunk(i,j,map_scalar*2,map_scalar)
				self.chunk_to_char(xmin,ymin,xmax,ymax)


# Testing
if __name__ == '__main__':
	class_test = ImageToAscii("../../data/map.jpg")
	class_test.open_image()
	class_test.convert_to_ascii(88,25)
