'''
Breakout

Instructions:
- Use the left and right arrow keys to control the player and bounce the ball
off the paddle
- Break the all of the blocks with ball
- Don't miss the ball more than 3 times or you lose

Aidan Clyens
June 21, 2018
'''
# Imports
import pygame
import random
import time

# Constants
WIDTH = 500
HEIGHT = 400
# Set number of rows and columns for blocks
ROWS = 4
COLUMNS = 30
# Object dimensions
BLOCK_WIDTH = WIDTH / COLUMNS
BLOCK_HEIGHT = BLOCK_WIDTH
BALL_HEIGHT = BLOCK_WIDTH
BALL_WIDTH = BALL_HEIGHT
PLAYER_WIDTH = BLOCK_WIDTH * 4
PLAYER_HEIGHT = BLOCK_HEIGHT
# Object speeds
PLAYER_SPEED = 6
BALL_SPEED = 4
# Colours
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Set the screen dimensions
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

'''
Block
Generated at the top of the screen
'''
class Block(object):
	# Block constructor
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT)
		self.colour = self.choose_colour()
	# Randomize the Block colour
	def choose_colour(self):
		num = random.randint(1,5)
		if num == 1:
			return RED
		elif num == 2:
			return GREEN
		elif num == 3:
			return BLUE
		elif num == 4:
			return (255,128,0)
		elif num == 5:
			return (0,128,255)

'''
Player
Controlled by the human player with the left and right arrow keys
'''
class Player(object):
	# Player constructor
	def __init__(self):
		self.x = (WIDTH / 2) - (BLOCK_WIDTH / 2)
		self.y = HEIGHT - BLOCK_HEIGHT
		self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
		self.colour = WHITE
		self.lives = 3
	# Draw Player on screen
	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
		pygame.draw.rect(SCREEN, self.colour, self.rect)
	# Update Player's movement
	def move(self):
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_LEFT]:
			if not self.x < 0: self.x -= PLAYER_SPEED
		if pressed[pygame.K_RIGHT]:
			if not self.x > WIDTH - PLAYER_WIDTH: self.x += PLAYER_SPEED

'''
Ball
'''
class Ball(object):
	# Ball constructor
	def __init__(self):
		self.reset()
		self.rect = pygame.Rect(self.x, self.y, BALL_WIDTH, BLOCK_HEIGHT)
		self.colour = WHITE
	# Draw Ball on screen
	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, BALL_WIDTH, BALL_HEIGHT)
		pygame.draw.rect(SCREEN, self.colour, self.rect)
	# Update Ball's movement
	def move(self, player, blocks):
		self.x += self.speed_x
		self.y += self.speed_y

		# Collision with side walls
		if self.x < 0 or self.x > WIDTH:
			self.speed_x *= -1
		# Collision with top wall
		if self.y < 0:
			self.speed_y *= -1
		# Collision with bottom wall
		if self.y > HEIGHT:
			player.lives -= 1
			self.reset()
		# Collision with player
		if self.rect.colliderect(player.rect):
			self.y = player.y - BALL_HEIGHT
			self.speed_y *= -1
			if (self.x + BALL_WIDTH / 2) < (player.x + PLAYER_WIDTH / 3) or (self.x - BALL_WIDTH / 2) > (player.x + 2 * PLAYER_WIDTH / 3):
				self.speed_x *= -1

		# Collision with block
		for block in blocks:
			if self.rect.colliderect(block.rect):
				blocks.remove(block)
				self.y = block.y + BALL_HEIGHT
				self.speed_y *= -1

	def reset(self):
		num = random.randint(0,1)
		if num == 0:
			self.speed_x = -1 * BALL_SPEED
		elif num == 1:
			self.speed_x = BALL_SPEED

		self.x = WIDTH / 2
		self.y = HEIGHT / 3
		self.speed_y = BALL_SPEED
		time.sleep(1)

'''
Local Functions
'''
# Add blocks to list
def add_blocks():
	blocks = []
	for row in range(0, ROWS + 1):
		for col in range(0, COLUMNS + 1):
			block = Block(col*BLOCK_WIDTH, row*BLOCK_HEIGHT)
			blocks.append(block)
	return blocks

# Draw all blocks in list on the screen
def draw_blocks(blocks):
	for i in range(0, len(blocks)):
		pygame.draw.rect(SCREEN, blocks[i].colour, blocks[i].rect)

'''
Main Function
'''
def main():
	# Start game
	pygame.init()
	running = True

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
		SCREEN.fill((0,0,0))
		draw_blocks(blocks)
		player.draw()
		ball.draw()

		# End game conditions
		if player.lives == 0:
			running = False

		if len(blocks) == 0:
			running = False

		# Update screen
		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
	quit()

if __name__ == '__main__':
	main()
