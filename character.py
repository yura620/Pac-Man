import basicSprite
from pygame.locals import *
import pygame


class Character(basicSprite.Sprite):
	"""This is our character that will move around the screen"""

	def __init__(self, centerPoint, image):
		"""initialize base class"""
		basicSprite.Sprite.__init__(self, centerPoint, image)

		"""Initialize the number of pellets collected"""
		self.pellets = 0

		"""Set the number of Pixels to move each time"""
		self.x_dist = 1
		self.y_dist = 1

		"""Initialize how much we are moving"""
		self.xMove = 0
		self.yMove = 0

		"""By default we are not in the "super" state"""
		self.superState = False

	def MoveKeyDown(self, key):
		"""This function sets the xMove or yMove variables that will
		then move the snake when update() function is called.  The
		xMove and yMove values will be returned to normal when this
		keys MoveKeyUp function is called."""

		if key == K_RIGHT:
			self.xMove += self.x_dist
		elif key == K_LEFT:
			self.xMove += -self.x_dist
		elif key == K_UP:
			self.yMove += -self.y_dist
		elif key == K_DOWN:
			self.yMove += self.y_dist

	def MoveKeyUp(self, key):
		"""This function resets the xMove or yMove variables that will
		then move the snake when update() function is called.  The
		xMove and yMove values will be returned to normal when this
		keys MoveKeyUp function is called."""

		if key == K_RIGHT:
			self.xMove += -self.x_dist
		elif key == K_LEFT:
			self.xMove += self.x_dist
		elif key == K_UP:
			self.yMove += self.y_dist
		elif key == K_DOWN:
			self.yMove += -self.y_dist

	def update(self, block_group, pellet_group):#, super_pellet_group, monster_group):
		"""Called when the Snake sprite should update itself"""

		if (self.xMove == 0) and (self.yMove == 0):
			"""If we aren't moving just get out of here"""
			return

		"""All right we must be moving!"""
		self.rect.move_ip(self.xMove, self.yMove)  # moves the rectangle, in place

		if pygame.sprite.spritecollideany(self, block_group):
			"""IF we hit a block, don't move - reverse the movement"""
			self.rect.move_ip(-self.xMove, -self.yMove)

		"""Check for a snake collision/pellet collision"""
		lstCols = pygame.sprite.spritecollide(self, pellet_group, True)

		"""Update the amount of pellets eaten"""
		self.pellets = self.pellets + len(lstCols)
