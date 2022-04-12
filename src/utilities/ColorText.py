"""
@author: Max Marshall
@desc:
@created: 04/12/2022
"""
#import


class ColorText:
	def __init__(self):
		self.reset = "\033[0m"
		self.fgcolor_map = {}
		self.bgcolor_map = {}
		self.special_map = {}
		# Foreground Colors
		self.fgcolor_map["wht"] = "37"
		self.fgcolor_map["red"] = "31"
		self.fgcolor_map["grn"] = "32"
		self.fgcolor_map["blu"] = "34"
		self.fgcolor_map["blk"] = "30"
		# Background Colors
		self.bgcolor_map["wht"] = "47"
		self.bgcolor_map["red"] = "41"
		self.bgcolor_map["grn"] = "42"
		self.bgcolor_map["blu"] = "44"
		self.bgcolor_map["blk"] = "40"
		# Special Modifiers
		self.special_map[""] = "0"
		self.special_map["bld"] = "1"
		self.special_map["uln"] = "4"
		self.special_map["bnk"] = "5"

	def set_color(self, fg, bg):
		if fg in self.fgcolor_map:
			self.fg = self.fgcolor_map[fg]
		else:
			self.fg = self.fgcolor_map["wht"]
		if bg in self.bgcolor_map:
			self.bg = self.bgcolor_map[bg]
		else:
			self.bg = self.bgcolor_map["blk"]
		
	def set_special(self, fg, bg):
		if fg in self.special_map:
			self.sp_fg = self.special_map[fg]
		else:
			self.sp_fg = "0"
		if bg in self.special_map:
			self.sp_bg = self.special_map[bg]
		else:
			self.sp_bg = "0"

	def print(self, string):
		print("\033[{0};{1};{2};{3}m{4}{5}".format(self.sp_fg,self.fg,self.sp_bg,self.bg,string,self.reset),end="")
		


# Testing
if __name__ == '__main__':
	class_test = ColorText()
