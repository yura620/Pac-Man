import basicSprite
from pygame.locals import *
import pygame
import time

SUPER_STATE_START = pygame.USEREVENT + 1
SUPER_STATE_OVER = pygame.USEREVENT + 2
CHARACTER_EATEN = pygame.USEREVENT + 3
PELLETS_COLLECTED = pygame.USEREVENT + 4


class Character(basicSprite.Sprite):
	"""This is our character that will move around the screen"""

	def __init__(self, centerPoint, image_list):
		self.image_list = image_list

		"""initialize base class"""
		basicSprite.Sprite.__init__(self, centerPoint, image_list[1])

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

		self.steps = 0

		self.superState = False
		self.superState_start = 0
		self.superState_length = 5

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

	def update(self, level, block_group, pellet_group, spellet_group, npc_group):
		"""Called when the character sprite should update itself"""

		"""Check to see if we hit a Monster!"""
		npc_lst = pygame.sprite.spritecollide(self, npc_group, False)

		if len(npc_lst) > 0:
			"""Alright we have hit a Monster!"""
			self.NpcCollide(npc_lst)

		if (self.xMove == 0) and (self.yMove == 0):
			"""If we aren't moving just get out of here"""
			return

		"""Add Pac-Man mouth motion while moving"""
		cur_image = self.image_list[1]
		if (self.steps >= 0) and (self.steps < 10):
			cur_image = self.image_list[1]
		elif (self.steps >= 10) and (self.steps < 20):
			cur_image = self.image_list[2]
		elif (self.steps >= 20) and (self.steps < 30):
			cur_image = self.image_list[0]
		elif (self.steps >= 30) and (self.steps < 40):
			cur_image = self.image_list[2]

		"""Rotate Pac-Man according movement direction"""
		if self.xMove > 0:
			self.image = cur_image
		elif self.xMove < 0:
			self.image = pygame.transform.rotate(cur_image, 180)
		elif self.yMove > 0:
			self.image = pygame.transform.rotate(cur_image, 270)
		elif self.yMove < 0:
			self.image = pygame.transform.rotate(cur_image, 90)

		"""All right we must be moving!"""
		self.rect.move_ip(self.xMove, self.yMove)  # moves the rectangle, in place

		if pygame.sprite.spritecollideany(self, block_group):
			"""IF we hit a block, don't move - reverse the movement"""
			# self.rect.move_ip(-self.xMove, -self.yMove)

			x = self.rect.center[0] // 24
			y = self.rect.center[1] // 24

			self.rect.center = level[y][x][0]
		else:
			if self.steps == 40:
				self.steps = 0
			else:
				self.steps += 1

		"""Check for a snake collision with pellet"""
		lstCols = pygame.sprite.spritecollide(self, pellet_group, True)

		"""Update the amount of pellets eaten"""
		self.pellets = self.pellets + len(lstCols)

		if self.pellets == 178:
			pygame.event.post(pygame.event.Event(PELLETS_COLLECTED, {}))

		"""Check for a snake collision with super pellet"""
		if len(pygame.sprite.spritecollide(self, spellet_group, True)):
			"""We have collided with a super pellet! Time to become Super!"""
			self.superState = True
			pygame.event.post(pygame.event.Event(SUPER_STATE_START, {}))

			"""Start a timer to figure out when the super state ends"""
			pygame.time.set_timer(SUPER_STATE_OVER, 0)
			pygame.time.set_timer(SUPER_STATE_OVER, 5000)

	def NpcCollide(self, npc_lst):
		"""This Function is called when the character collides with the npc
		lst npc is a list of npc sprites that it has hit."""

		if len(npc_lst) <= 0:
			"""If the list is empty, just get out of here"""
			return

		"""Loop through the monsters and see what should happen"""
		for npc in npc_lst:
			if npc.scared:
				npc.Eaten()
			else:
				"""Looks like we're dead"""
				pygame.event.post(pygame.event.Event(CHARACTER_EATEN, {}))
