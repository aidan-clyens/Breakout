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

# Constants
WIDTH = 500
HEIGHT = 400
# Set number of rows and columns for blocks
ROWS = 4
COLUMNS = 15
# Object dimensions
BLOCK_WIDTH = WIDTH / COLUMNS
BLOCK_HEIGHT = BLOCK_WIDTH / 2
BALL_HEIGHT = BLOCK_HEIGHT
BALL_WIDTH = BALL_HEIGHT
PLAYER_WIDTH = BLOCK_HEIGHT * 4
PLAYER_HEIGHT = BLOCK_HEIGHT
# Object speeds
PLAYER_SPEED = 6
BALL_SPEED = 4
# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)
MAGENTA = (255,0,255)

# Set the screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

""" Block
Generated at the top of the screen
"""
class Block():
	# Block constructor
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.colour = self.choose_colour()
		self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
		self.image.fill(self.colour)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	# Draw the Block
	def draw(self):
		pygame.draw.rect(screen, self.colour, self.rect)

	# Randomize the Block colour
	def choose_colour(self):
		# Choose between 1 of 5 different colours by generating a pseudorandom integer between 1 and 5
		num = random.randint(1,5)
		if num == 1:
			return RED
		elif num == 2:
			return GREEN
		elif num == 3:
			return BLUE
		elif num == 4:
			return ORANGE
		elif num == 5:
			return MAGENTA

""" Player
Controlled by the human player with the left and right arrow keys
"""
class Player():
	# Initialize the Player position to the bottom of the screen and centered horizontally
	x = (WIDTH / 2) - (BLOCK_WIDTH / 2)
	y = HEIGHT - BLOCK_HEIGHT
	colour = WHITE

	# Player constructor
	def __init__(self):
		self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
		self.image.fill(self.colour)
		self.rect = self.image.get_rect()
		self.lives = 3
		self.rect.x = self.x
		self.rect.y = self.y
	# Draw Player on screen
	def draw(self):
		self.rect.x = self.x
		self.rect.y = self.y
		pygame.draw.rect(screen, self.colour, self.rect)
	# Update Player's movement
	def move(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_LEFT]:
			if not self.x < 0: self.x -= PLAYER_SPEED
		if pressed[pygame.K_RIGHT]:
			if not self.x > WIDTH - PLAYER_WIDTH: self.x += PLAYER_SPEED

""" Ball
"""
class Ball():
	# Initialized the Ball position to the center of the screen horizontally and 2/3 down the screen vertically
	colour = WHITE
	x = WIDTH / 2
	y = HEIGHT / 3

	# Ball constructor
	def __init__(self):
		self.image = pygame.Surface([BALL_WIDTH, BALL_HEIGHT])
		self.image.fill(self.colour)
		self.rect = self.image.get_rect()
		self.reset()

	# Draw Ball on screen
	def draw(self):
		pygame.draw.rect(screen, self.colour, self.rect)

	# Update Ball's movement
	def move(self, player, blocks):
		self.rect.x += self.dx
		self.rect.y += self.dy

		# Collision with left wall
		if self.rect.left < 0:
			self.dx *= -1
			self.rect.x += 2
		# Collision with right wall
		if self.rect.right > WIDTH:
			self.dx *= -1
			self.rect.x -= 2
		# Collision with top wall
		if self.rect.top < 0:
			self.dy *= -1
		# Collision with bottom wall
		if self.rect.top > HEIGHT:
			player.lives -= 1
			self.reset()

		# Collision with Player
		if self.rect.colliderect(player.rect):
			# Ball hits side of Player
			if self.rect.bottom - player.rect.top > 1:
				self.dx *= -1
			else:
				self.dy *= -1
				self.rect.y += 2
				if self.rect.right > player.rect.right: self.dx *= -1
				if self.rect.left < player.rect.left: self.dx *= -1


		# Collision with Blocks
		for block in blocks:
			if self.rect.colliderect(block.rect):
				# Ball hits side of Block
				if block.rect.bottom - self.rect.top > 3:
					print "side"
					self.dx *= -1
				else:
					print "bottom"
					self.dy *= -1
					self.rect.y += 2

				blocks.remove(block)



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
				block = Block(col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
				blocks.append(block)
	return blocks

# Draw all blocks in list on the screen
def draw_blocks(blocks):
	for i in range(0, len(blocks)):
		blocks[i].draw()

"""Main Function
"""
def main():
	# Start game
	pygame.init()
	running = True

	background = pygame.image.load('arcade-background.jpg')

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

		# Move objects
		player.move()
		ball.move(player, blocks)

		# Draw screen and objects
		screen.blit(background, (0,0))
		draw_blocks(blocks)
		player.draw()
		ball.draw()

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
