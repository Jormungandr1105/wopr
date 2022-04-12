"""
@author: Max Marshall
@desc: Main file for wopr, a program inspired by the movie WarGames
@created: 04/12/2022
"""
from utilities.ColorText import *


def run():
	printer = ColorText()
	printer.set_color("wht","blk")
	printer.set_special("bnk","bnk")
	printer.print("DO YOU WANT TO PLAY A GAME?\n")

if __name__ == '__main__':
	run()
