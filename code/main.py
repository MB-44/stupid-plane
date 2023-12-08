import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from os import listdir
from os.path import join, isfile


class Game:
	def __init__(self):

		# setup
		pygame.init()
		self.displaySurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption("Stupid Plane")
		self.clock = pygame.time.Clock()
		self.active = True

		# sprite groups
		self.allSprites = pygame.sprite.Group()
		self.collisionSprites = pygame.sprite.Group()

		# scale factor
		bgHeight = pygame.image.load(join("graphics","environment","background.png")).get_height()
		self.scaleFactor = WINDOW_HEIGHT / bgHeight

		# sprite setup
		BG(self.allSprites,self.scaleFactor)
		Ground([self.allSprites,self.collisionSprites],self.scaleFactor)
		self.plane = Plane(self.allSprites,self.scaleFactor/1.7)

		# timer
		self.obstacleTimer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacleTimer,1400)

		# text
		self.font = pygame.font.Font(join("graphics","font","BD_Cartoon_Shout.ttf"),30)
		self.score = 0
		self.startOffset = 0

		# menu
		self.menuSurf = pygame.image.load(join("graphics","ui","menu.png")).convert_alpha()
		self.menuRect = self.menuSurf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_WIDTH / 2))
		
		# music 
		self.music = pygame.mixer.Sound(join("sounds","music.wav"))
		self.music.play(loops = -1)

	def collisions(self):
		if pygame.sprite.spritecollide(self.plane,self.collisionSprites,False,pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
			for sprite in self.collisionSprites.sprites():
				if sprite.sprite_type == 'obstacle': # sprite_type = 'obstacle'
					sprite.kill()
			self.active = False
			self.plane.kill()

	def displayScore(self):
		if self.active:
			self.score = (pygame.time.get_ticks() - self.startOffset) // 1000
			y = WINDOW_HEIGHT / 10
		else:
			y = WINDOW_HEIGHT / 2 + (self.menuRect.height / 1.5)

		scoreSurf = self.font.render(str(self.score),True,'black')
		scoreRect = scoreSurf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
		self.displaySurface.blit(scoreSurf,scoreRect)

	def run(self):
		lastTime = time.time()
		while True:
			
			# delta time
			dt = time.time() - lastTime
			lastTime = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.active:
						self.plane.jump()
					else:
						self.plane = Plane(self.allSprites,self.scaleFactor / 1.7)
						self.active = True
						self.startOffset = pygame.time.get_ticks()

				if event.type == self.obstacleTimer and self.active:
					Obstacle([self.allSprites,self.collisionSprites],self.scaleFactor * 1.1)
			
			# game logic
			self.displaySurface.fill('black')
			self.allSprites.update(dt)
			self.allSprites.draw(self.displaySurface)
			self.displayScore()

			if self.active: 
				self.collisions()
			else:
				self.displaySurface.blit(self.menuSurf,self.menuRect)

			pygame.display.update()
			# self.clock.tick(FRAMERATE)


if __name__ == '__main__':
	game = Game()
	game.run()



	   