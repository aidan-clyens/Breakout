"""Breakout

Instructions:
- Use the left and right arrow keys to control the player and bounce the ball
off the paddle
- Break the all of the blocks with ball
- Don't miss the ball more than 3 times or you lose

Aidan Clyens
July 23, 2018
"""
# Imports
import pygame
import random
import time
from constants import *

background_image = 'arcade-background.jpg'

# Set the screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

paused = False
running = False

""" Block
Generated at the top of the screen
"""
class Block():
	# Block constructor
	def __init__(self, x, y, w, h, colour):
		self.image = pygame.Surface([w, h])
		self.image.fill(colour)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.w = w
		self.h = h

	# Draw the Block
	def draw(self):
		screen.blit(self.image, [self.rect.x, self.rect.y])

	def update(self):
		self.draw()

	def test_collision(self, blocks):
		collisions = []
		for block in blocks:
			if self.rect.colliderect(block.rect):
				collisions.append(block)

		return collisions

class LevelBlock(Block):
	def __init__(self, x, y):
		row = y / BLOCK_HEIGHT
		Block.__init__(self, x, y, BLOCK_WIDTH, BLOCK_HEIGHT, self.choose_colour(row))

	def update(self):
		Block.update(self)

	# Randomize the Block colour
	def choose_colour(self, row):
		# Choose between 1 of 5 different colours by generating a pseudorandom integer between 1 and 5
		if row == 1:
			return RED
		if row == 2:
			return ORANGE
		if row == 3:
			return YELLOW
		if row == 4:
			return GREEN
		if row >= 5:
			return BLUE
		
		return WHITE

""" Player
Controlled by the human player with the left and right arrow keys
"""
class Player(Block):
	# Player constructor
	def __init__(self):
		x = WIDTH / 2
		y = HEIGHT - PLAYER_HEIGHT
		Block.__init__(self, x, y, PLAYER_WIDTH, PLAYER_HEIGHT, RED)
		self.lives = 3

	# Draw Player on screen
	def update(self):
		self.move()
		Block.update(self)

	# Update Player's movement
	def move(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_a]:
			if not self.rect.x < 0: self.rect.x -= PLAYER_SPEED
		if pressed[pygame.K_d]:
			if not self.rect.x > WIDTH - PLAYER_WIDTH: self.rect.x += PLAYER_SPEED

""" Ball
"""
class Ball(Block):
	# Ball constructor
	def __init__(self):
		x = WIDTH / 2
		y = HEIGHT / 3
		Block.__init__(self, x, y, BALL_WIDTH, BALL_HEIGHT, RED)
		self.reset()

	# Draw Ball on screen
	def update(self, player, blocks):
		self.move(player, blocks)
		Block.update(self)

	def moveX(self, player, blocks):
		# x-Axis Movement
		self.rect.x += self.dx

		# Collision with left wall
		if self.rect.left < 0:
			self.dx *= -1
			self.rect.x += 2
		# Collision with right wall
		if self.rect.right > WIDTH:
			self.dx *= -1
			self.rect.x -= 2

		collisions = self.test_collision(blocks)
		for block in collisions:
			# Moving right
			if self.dx > 0:
				self.rect.right = block.rect.left
			# Moving left
			if self.dx < 0:
				self.rect.left = block.rect.right
			self.dx *= -1
			blocks.remove(block)
			break

		if self.rect.colliderect(player.rect):
			# Moving up
			if self.dx > 0:
				self.rect.right = player.rect.left
			# Moving down
			if self.dx < 0:
				self.rect.left = player.rect.right
			self.dx *= -1

	def moveY(self, player, blocks):
		self.rect.y += self.dy

		# Collision with top wall
		if self.rect.top < 0:
			self.dy *= -1
		# Collision with bottom wall
		if self.rect.top > HEIGHT:
			player.lives -= 1
			self.reset()

		collisions = self.test_collision(blocks)
		for block in collisions:
			# Moving down
			if self.dy > 0:
				self.rect.bottom = block.rect.top
			# Moving up
			if self.dy < 0:
				self.rect.top = block.rect.bottom
			self.dy *= -1
			blocks.remove(block)
			break

		if self.rect.colliderect(player.rect):
			# Moving down
			if self.dy > 0:
				self.rect.bottom = player.rect.top
			# Moving up
			if self.dy < 0:
				self.rect.top = player.rect.bottom
			self.dy *= -1


	# Update Ball's movement
	def move(self, player, blocks):
		self.moveX(player, blocks)
		self.moveY(player, blocks)

	# Reset the Ball's position
	def reset(self):
		num = random.randint(0,1)
		if num == 0:
			self.dx = -1 * BALL_SPEED
		elif num == 1:
			self.dx = BALL_SPEED

		self.rect.x = WIDTH / 2
		self.rect.y = HEIGHT / 3
		self.dy = BALL_SPEED
		time.sleep(1)

"""Local Functions
"""
# Add blocks to list
def add_blocks():
	blocks = []
	for row in range(0, ROWS + 1):
		if row > 0:
			for col in range(0, COLUMNS + 1):
				block = LevelBlock(col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
				blocks.append(block)
	return blocks

"""Main Function
"""
def main():
	# Start game
	pygame.init()
	running = True

	background = pygame.image.load(background_image)

	# Create a new clock and add all objects to the game
	clock = pygame.time.Clock()
	blocks = add_blocks()
	player = Player()
	ball = Ball()
	# Game loop
	while running:
		# Handle game events
		for event in pygame.event.get():
				# Quit the game when the window is closed
	    		if event.type == pygame.QUIT:
	        		running = False

		# Draw screen and objects
		# screen.blit(background, (0,0))
		screen.fill(BLACK)

		for block in blocks:
			block.update()
		player.update()
		ball.update(player, blocks)

		# End game conditions
		if player.lives == 0:
			running = False

		if len(blocks) == 0:
			running = False

		# Update screen at 60 FPS
		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
	quit()

if __name__ == '__main__':
	main()
