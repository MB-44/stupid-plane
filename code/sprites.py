from msilib.schema import SelfReg
import random
from typing import Self
from matplotlib.scale import scale_factory
import pygame 
from settings import *
from random import choice, randint
from os import listdir
from os.path import join, isfile

class BG(pygame.sprite.Sprite):
	def __init__(self,groups,scaleFactor):
		super().__init__(groups)
		bgImage = pygame.image.load(join("graphics","environment","background.png")).convert()

		fullHeight = bgImage.get_height() * scaleFactor
		fullWidth = bgImage.get_width() * scaleFactor
		fullSizedImage = pygame.transform.scale(bgImage,(fullWidth,fullHeight))
		
		self.image = pygame.Surface((fullWidth * 2,fullHeight))
		self.image.blit(fullSizedImage,(0,0))
		self.image.blit(fullSizedImage,(fullWidth,0))

		self.rect = self.image.get_rect(topleft = (0,0))
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def update(self,dt):
		self.pos.x -= 300 * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0
		self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
	def __init__(self,groups,scaleFactor):
		super().__init__(groups)
		self.spriteType = 'ground'
		
		# image
		groundSurf = pygame.image.load(join("graphics","environment","ground.png")).convert_alpha()
		self.image = pygame.transform.scale(groundSurf,pygame.math.Vector2(groundSurf.get_size()) * scaleFactor)
		
		# position
		self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.pos.x -= 360 * dt
		if self.rect.centerx <= 0:
			self.pos.x = 0

		self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
	def __init__(self,groups,scaleFactor):
		super().__init__(groups)

		# image 
		self.import_frames(scaleFactor)
		self.frameIndex = 0
		self.image = self.frames[self.frameIndex]

		# rect
		self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20,WINDOW_HEIGHT / 2))
		self.pos = pygame.math.Vector2(self.rect.topleft)

		# movement
		self.gravity = 600
		self.direction = 0

		# mask
		self.mask = pygame.mask.from_surface(self.image)

		# sound
		self.jumpSound = pygame.mixer.Sound(join("sounds","jump.wav"))
		self.jumpSound.set_volume(0.3)

	def import_frames(self,scaleFactor):
		self.frames = []
		for i in range(3):
			surf = pygame.image.load(join("graphics","plane",f"red{i}.png")).convert_alpha()
			scaledSurface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scaleFactor)
			self.frames.append(scaledSurface)

	def apply_gravity(self,dt):
		self.direction += self.gravity * dt
		self.pos.y += self.direction * dt
		self.rect.y = round(self.pos.y)

	def jump(self):
		self.jumpSound.play()
		self.direction = -400

	def animate(self,dt):
		self.frameIndex += 10 * dt
		if self.frameIndex >= len(self.frames):
			self.frameIndex = 0
		self.image = self.frames[int(self.frameIndex)]

	def rotate(self):
		rotatedPlane = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1)
		self.image = rotatedPlane
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.apply_gravity(dt)
		self.animate(dt)
		self.rotate()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,groups,scaleFactor):
		super().__init__(groups)
		orientation = choice(('up','down'))
		
		surf = pygame.image.load(join("graphics","obstacles",f"{choice((0,1))}.png")).convert_alpha()
		self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scaleFactor)
		self.sprite_type = 'obstacle'
		
		x = WINDOW_WIDTH + randint(40,100)

		if orientation == 'up':
			y = WINDOW_HEIGHT + randint(10,50)
			self.rect = self.image.get_rect(midbottom = (x,y))
		else:
			y = randint(-50,-10)
			self.image = pygame.transform.flip(self.image,False,True)
			self.rect = self.image.get_rect(midtop = (x,y))

		self.pos = pygame.math.Vector2(self.rect.topleft)

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,dt):
		self.pos.x -= 400 * dt
		self.rect.x = round(self.pos.x)
		if self.rect.right <= -100:
			self.kill()
