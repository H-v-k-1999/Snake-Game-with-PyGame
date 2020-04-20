import pygame # Importing the pygame module (Make sure you first install it using pip install pygame).
import random # Using random to generate apples at random position

pygame.init() # Initializing the pygame module

WIDTH, HEIGHT = 800, 600 #Setting the width and height of the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Awesome Snake Game") # Giving the title to the game window

clock = pygame.time.Clock() # Initializing the pygame clock to handle the game FPS.

# Defining the Direction Constants
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# The Snake Class
class Snake(object):

	def __init__(self, x, y, length, color):
		self.x = x
		self.y = y
		self.length = length
		self.size = 10 # Scale of the snake
		self.color = color
		self.head = (self.x, self.y)
		self.trace = [self.head] # This stores the coordiantes of the entire body of the snake.
		self.direction = DOWN # Default direction unless a direction specifying key is pressed.

	def move(self, movement):
		if movement == UP:
			self.y -= self.size
		elif movement == DOWN:
			self.y += self.size
		elif movement == LEFT:
			self.x -= self.size
		elif movement == RIGHT:
			self.x += self.size

		self.head = (self.x, self.y) # Modifying the location of the head after each move.
		self.trace.append(self.head) # Appending the new head of the snake to the trace.

	def draw(self, win):
		# Drawing all the parts of the snake.
		for t in self.trace:
			pygame.draw.rect(win, self.color, (t[0], t[1], self.size, self.size))

		# Coloring the head of the snake.
		pygame.draw.rect(win, (3, 252, 7), (self.head[0], self.head[1], self.size, self.size))

# The Apple Class
class Apple(object):

	def __init__(self, color):
		self.color = color
		self.size = 10
		# Randomly generating the X and Y coordinate for the apple.
		self.x = random.randint(0, WIDTH // self.size - 1) * self.size
		self.y = random.randint(0, HEIGHT // self.size - 1) * self.size
		# Creating a visibility variable to give a eating animation.
		self.visible = True

	def draw(self, win):
		# Drawing the apple.
		pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))


def reDrawGameWindow():

	# The pause screen.
	if paused and not gameOver:
		textPaused = font.render('P A U S E D', 1, (255,0,0)) # Generating the 'P A U S E D' text.
		win.blit(textPaused, (WIDTH/2 - (textPaused.get_width()/2), HEIGHT/2)) # Displaying the 'P A U S E D' text.

	# The game over screen.
	if gameOver:
		textGameOver = font.render('G A M E   O V E R', 1, (255,0,0)) # Generating the 'G A M E   O V E R' text.
		textScore = font.render('Score : ' + str(SCORE), 1, (255,255,255)) # Generating the 'G A M E   O V E R' text.
		textLength = font.render('Length : ' + str(snake.length), 1, (255,255,255)) # Generating the 'G A M E   O V E R' text.
		win.blit(textGameOver, (WIDTH/2 - (textGameOver.get_width()/2), HEIGHT/2 - 30)) # Displaying the 'G A M E   O V E R' text.
		win.blit(textScore, (WIDTH/2 - (textScore.get_width()/2), HEIGHT/2)) # Displaying the score.
		win.blit(textLength, (WIDTH/2 - (textLength.get_width()/2), HEIGHT/2 + 30)) # Displaying the length of the snake.

	if not gameOver and not paused:
		if to_remove:
			snake.trace.remove(snake.trace[0])
		snake.draw(win) # Drawing the snake on our game window.
		apple.draw(win) # Drwaing the apple in our game window.
	pygame.display.update() # VERY IMPORTANT!!! Updating the window to display all the drawn objects.
	win.fill((0,0,0)) # CLearing the screen to draw the objects on updated location.

run = True # A variable to help in exiting the loop.
snake = Snake(100, 30, 1, (0, 158, 3)) # Creating the Snake class object.
apple = Apple((252, 33, 33)) # Creating the Apple class object.
SCORE = 0 # Counter to keep the score.
font = pygame.font.SysFont('ComicSans', 30, True, True) # Initializing a font.
DEBUG = False # To print statement while in the debug state.
to_remove = True # To decide whether to remove the tail of the snake.
gameOver = False # To check when the game is over.
paused = False # To check when the game is paused.

while run:
	if DEBUG:
		print('Snake location : x =', snake.head[0], 'y =', snake.head[1])
		print('Apple location : x =', apple.x, 'y =', apple.y)
		print(snake.direction)

	clock.tick(25 + SCORE) # Increasing the speed of the snake.
	keys = pygame.key.get_pressed() # Capturing the keys currently pressed on the keyboard.

	if not paused:

		# To check if the snake ate the apple
		if apple.x == snake.x and apple.y == snake.y:
			apple.visible = False # Making the apple invisible if it got eaten.
			snake.length += 1 # Incrementing the length of the snake.
			SCORE += 1 # Incrementing the score.
			to_remove = False # So that the last part of the snake is not erased.
		else:
			to_remove = True # To normally remove the last part of the snake.

		# To make an apple appear after the current one got eaten.
		if not apple.visible:
			apple = Apple((252, 33, 33))
			while (apple.x, apple.y) in snake.trace: # While the apple's location is on the snake body creating a new apple.
				apple = Apple((252, 33, 33))

		if not gameOver:

			# To check which key is being pressed on the keyboard.
			if keys[pygame.K_UP] and snake.direction != DOWN:
				snake.direction = UP
			elif keys[pygame.K_DOWN] and snake.direction != UP:
				snake.direction = DOWN
			elif keys[pygame.K_LEFT] and snake.direction != RIGHT:
				snake.direction = LEFT
			elif keys[pygame.K_RIGHT] and snake.direction != LEFT:
				snake.direction = RIGHT

			# This series of statement will make the snake appear at the other end.
			if snake.x >= WIDTH:
				snake.x = 0
			if snake.y >= HEIGHT:
				snake.y = 0
			if snake.x < 0:
				snake.x = WIDTH
			if snake.y < 0:
				snake.y = HEIGHT

			snake.move(snake.direction) # Moving the snake according to the direction.

		if snake.head in snake.trace[:-1]: # Checking the collision with its own tail.
			gameOver = True

	reDrawGameWindow() # Calling the redraw function.

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # To check if the X button is clicked on the screen.
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: # To check if the spacebar is pressed.
				paused = not paused # Altering the pause so game can be bought back from pause.

pygame.quit()