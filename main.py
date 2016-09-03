import sys
from pygame.locals import *
import pygame
import level
import basicSprite
from character import *
import time
import npc

if not pygame.font:
	print('Warning, fonts disabled')
if not pygame.mixer:
	print('Warning, sound disabled')

BLOCK_SIZE = 24


class GameMain:
	"""The Main PyMan Class - This class handles the main initialization and creating of the Game."""

	def __init__(self, curLevel):
		"""Initialize"""

		"""Load level info"""
		self.level = level.Level(curLevel)

		"""Set the window Size"""
		self.width = self.level.width
		self.height = self.level.height

		"""Set block size"""
		self.BLOCK_SIZE = self.level.blockSize

		"""Initialize PyGame"""
		pygame.init()

		"""Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))

		self.background = None
		self.layout = None
		self.sprites_block = None
		self.character = None
		self.sprites_character = None
		self.sprites_pellet = None
		self.sprites_spellet = None
		self.npc = None
		self.sprites_npc = None

	def MainLoop(self):
		"""This is the Main Loop of the Game"""

		"""Load the level"""
		self.layout = self.level.getLayout()

		"""Load All of our Sprites"""
		self.LoadSprites()

		"""Create the background"""
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))

		"""Draw the blocks onto the background, since they only need to be drawn once"""
		self.sprites_block.draw(self.background)

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if (event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN):
						self.character.MoveKeyDown(event.key)
				elif event.type == KEYUP:
					if (event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN):
						self.character.MoveKeyUp(event.key)
				elif event.type == SUPER_STATE_OVER:
					self.character.superState = False
					"""Stop the timer"""
					pygame.time.set_timer(SUPER_STATE_OVER, 0)
					for n_p_c in self.sprites_npc.sprites():
						n_p_c.SetScared(False)
				elif event.type == SUPER_STATE_START:
					for n_p_c in self.sprites_npc.sprites():
						n_p_c.SetScared(True)
				elif event.type == SNAKE_EATEN:
					"""The character is dead!"""
					"""For now just quit"""
					return  # sys.exit()

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						return  # sys.exit()
					elif event.type == KEYDOWN:
						if event.key == K_p:
							self.Pause()

			"""Update the snake sprite"""
			self.sprites_character.update(self.layout, self.sprites_block, self.sprites_pellet, self.sprites_spellet, self.sprites_npc)

			"""Update NPC sprites"""
			self.sprites_npc.update(self.sprites_block)

			"""Do the Drawing"""
			self.screen.blit(self.background, (0, 0))		# draw one image onto another
			self.sprites_character.draw(self.screen)
			self.sprites_pellet.draw(self.screen)
			self.sprites_spellet.draw(self.screen)
			self.sprites_npc.draw(self.screen)
			if pygame.font:
				font = pygame.font.Font(None, 36)
				text = font.render("Pellets %s" % self.character.pellets, 1, (255, 0, 0))
				textpos = text.get_rect(centerx=self.background.get_width() / 2)
				self.screen.blit(text, textpos)
			pygame.display.flip()							# Update the full display Surface to the screen

			time.sleep(0.005)

	def LoadSprites(self):
		"""Load all of the sprites that we need"""

		"""Load textures"""
		img_list = self.level.getSprites()

		"""Create the group of block sprites"""
		self.sprites_block = pygame.sprite.Group()

		"""Create the group of pellet sprites"""
		self.sprites_pellet = pygame.sprite.Group()

		"""Create the group of super-pellet sprites"""
		self.sprites_spellet = pygame.sprite.Group()

		"""Create the group of npc sprites"""
		self.sprites_npc = pygame.sprite.Group()

		for y in range(len(self.layout)):
			for x in range(len(self.layout[y])):
				if self.layout[y][x][1] == self.level.BLOCK:
					block = basicSprite.Sprite(self.layout[y][x][0], img_list[self.level.BLOCK])
					self.sprites_block.add(block)
				elif self.layout[y][x][1] == self.level.CHARACTER:
					self.character = Character(self.layout[y][x][0], img_list[self.level.CHARACTER])
				elif self.layout[y][x][1] == self.level.PELLET:
					pellet = basicSprite.Sprite(self.layout[y][x][0], img_list[self.level.PELLET])
					self.sprites_pellet.add(pellet)
				elif self.layout[y][x][1] == self.level.SPELLET:
					spellet = basicSprite.Sprite(self.layout[y][x][0], img_list[self.level.SPELLET])
					self.sprites_spellet.add(spellet)
				elif self.layout[y][x][1] == self.level.NPC:
					self.npc = npc.NPC(self.layout[y][x][0], img_list[self.level.NPC])
					self.sprites_npc.add(self.npc)

		"""Create the Snake group"""
		self.sprites_character = pygame.sprite.RenderPlain(self.character)

	def Pause(self):
		"""Called when "p" button is pressed"""

		width = 150
		height = 50

		"""Draw a solid rectangle"""
		rect = [self.width / 2 - width / 2, self.height / 2 - height / 2, width, height]
		pygame.draw.rect(self.screen, (255, 0, 0), rect, 5)

		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render("Pause", 1, (255, 0, 0))
			textpos = text.get_rect(centerx=self.width / 2, centery=self.height / 2)
			#textpos.centerx = self.screen.get_rect().centerx
			#textpos.centery = self.screen.get_rect().centery
			self.screen.blit(text, textpos)

		pygame.display.flip()  # Update the full display Surface to the screen

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_p:
						return

if __name__ == "__main__":
	gameMain = GameMain('Level001')
	gameMain.MainLoop()

	print("End")
