import pygame
import basicSprite
import random


class NPC(basicSprite.Sprite):
	"""This is our NPC (Non Player Character) that will move around the screen"""

	def __init__(self, centerPoint, images_set):

		basicSprite.Sprite.__init__(self, centerPoint, images_set[0])

		"""Save the original rect (start position)"""
		self.original_rect = pygame.Rect(self.rect)
		self.normal_image = images_set[0]
		self.scared_image = images_set[1]

		self.scared = False

		"""Initialize the direction"""
		self.direction = random.randint(1, 4)		# random integer between 1 and 4
		self.dist = 1
		self.moves = random.randint(100, 200)		# number of moves after which NPC will choose another random direction
		self.moveCount = 0

	def update(self, block_group):
		"""Called when the NPC sprite should update itself"""
		xMove, yMove = 0, 0

		if self.direction == 1:				# move left
			xMove = -self.dist
		elif self.direction == 2:			# move up
			yMove = -self.dist
		elif self.direction == 3:			# move right
			xMove = self.dist
		elif self.direction == 4:			# move down
			yMove = self.dist

		self.rect.move_ip(xMove, yMove)		# Move the Rect
		self.moveCount += 1					# Update the Move count

		if pygame.sprite.spritecollideany(self, block_group):
			"""IF we hit a block, don't move - reverse the movement"""
			self.rect.move_ip(-xMove, -yMove)
			self.direction = random.randint(1, 4)
		elif self.moves == self.moveCount:
			"""If we have moved enough, choose a new direction"""
			self.direction = random.randint(1, 4)
			self.moves = random.randint(100, 200)
			self.moveCount = 0

	def SetScared(self, scared):
		"""Tell the NPC to be scared or not"""

		"""Should we update out scared image?"""
		if self.scared != scared:
			self.scared = scared
			if scared:
				self.image = self.scared_image
				self.dist = 0
			else:
				self.image = self.normal_image
				self.dist = 1

	def Eaten(self):
		"""Well looks like we've been eaten!, reset to the original
		position and stop being scared"""
		self.rect = self.original_rect
		self.scared = False
		self.dist = 1
		self.image = self.normal_image
