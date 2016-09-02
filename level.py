import os
import levelBase
from helpers import load_image


class Level(levelBase.Level):
	"""Level 1 of the PyMan Game"""

	def __init__(self, level):
		self.level = level
		self.BLOCK = 0
		self.CHARACTER = 1
		self.PELLET = 2
		self.SPELLET = 3

		fullname = os.path.join('data', 'maps', self.level)
		fullname = os.path.join(fullname, 'info')

		with open(fullname) as f:
			lines = f.read().splitlines()

		int_list = [int(i) for i in lines]

		self.width = int_list[0]
		self.height = int_list[1]
		self.blockSize = int_list[2]
		self.textures = int_list[3]

	def getLayout(self):
		fullname = os.path.join('data', 'maps', self.level)
		fullname = os.path.join(fullname, 'layout.lvl')

		"""Get block types"""
		with open(fullname) as f:
			bt = []
			for line in f:
				line = line.split()		# to deal with blank
				if line:				# lines (ie skip them)
					line = [int(i) for i in line]
					bt.append(line)

		x_offset = (self.blockSize / 2)
		y_offset = (self.blockSize / 2)

		"""Get layout [[block center x, block center y], block type]"""
		layout = []
		for y in range(len(bt)):
			line = []
			for x in range(len(bt[y])):
				"""Get the center point for the rects"""
				centerPoint = [(x * self.blockSize) + x_offset, (y * self.blockSize + y_offset)]

				line.append([centerPoint, bt[y][x]])
			layout.append(line)

		return layout

	def getSprites(self):
		if self.textures == 0:
			path = os.path.join('data', 'images')
		elif self.textures == 1:
			path = os.path.join('data', 'maps', self.level, 'images')

		block, rect = load_image(os.path.join(path, 'block.png'))
		character01, rect = load_image(os.path.join(path, 'character01.png'), -1)
		character02, rect = load_image(os.path.join(path, 'character02.png'), -1)
		character03, rect = load_image(os.path.join(path, 'character03.png'), -1)
		character = [character01, character02, character03]
		pellet, rect = load_image(os.path.join(path, 'pellet.png'), -1)
		spellet, rect = load_image(os.path.join(path, 'super_pellet.png'), -1)
		return [block, character, pellet, spellet]
