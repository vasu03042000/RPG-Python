import pygame
import time

#check for any contact between the player and any other game objects
def checkContact(x,y,objectImageX,objectImageY):
	global screen,textWin
	contactState = False
	if y >= objectImageY and y <= objectImageY + 50: #we are checking the head of the player

			if x >= objectImageX and x <= objectImageX + 40: #we are checking the left end of the player
				y = 650 #reset the player position
				contactState = True
			elif x+40 >= objectImageX and x+40 <= objectImageX + 40: #we are checking the right end of the player
				y = 650 #reset the player position
				contactState = True
	elif y + 50 >= objectImageY and y + 50 <= objectImageY + 50: #we are checking the back of the player
			if x >= objectImageX and x <= objectImageX + 40: #we are checking the left end of the player
				y = 650 #reset the player position
				contactState = True
			elif x + 40 >= objectImageX and x + 40 <= objectImageX + 40: #we are checking the right end of the player
				y = 650 #reset the player position
				contactState = True
	return contactState,y

#initiate the pygame library
pygame.init()
#set up a screen
screen = pygame.display.set_mode((900,700)) #(width,height)
#check whether game is over or not
finished = False #game not over
#initiate game level
level = 1
x = 420
y = 650
#load the player image
playerImage = pygame.image.load("beetle.png")
#resize the player image
playerImage = pygame.transform.scale(playerImage,(40,50))
#ready the image for integration
playerImage = playerImage.convert_alpha() #convert_alpha() specifically removes the background of the image icon so as to just focus on the image
#load the enemy image
enemyImage = pygame.image.load("enemy.png")
#resize the enemy image
enemyImage = pygame.transform.scale(enemyImage,(40,50))
#remove the extra background space of the image icon
enemyImage = enemyImage.convert_alpha()
#load the background image
backgroundImage = pygame.image.load("ground (1).jpg")
#resize the background image
backgroundImage = pygame.transform.scale(backgroundImage,(900,700))
#load the treasure image
treasureImage = pygame.image.load("treasure.png")
#resize the image
treasureImage = pygame.transform.scale(treasureImage,(40,50))
#remove extra background space of the image icon
treasureImage = treasureImage.convert_alpha()
#give the treasure an x and y coordinate
treasureImageX = 420
treasureImageY = 50
#give the enemy an x and y coordinate
enemyImageX = 500
enemyImageY = 450
#check the moving condition of the enemy
movingRight = False
#create a list containing inital enemy
enemyList = [(enemyImageX,enemyImageY,movingRight)]
#this remains the background image by default
screen.blit(backgroundImage,(0,0))
#declare a font object
font = pygame.font.SysFont("ariel",60)
#declare a frame rate
frame = pygame.time.Clock()
while finished == False: #while game is running
	for event in pygame.event.get(): #get all the events and go over them one by one
		if event.type == pygame.QUIT: #check if the event type is quit
			finished = True #exit the game
	
	#get the list of keys at the keyboard
	pressed_keys = pygame.key.get_pressed() #This will return the list of pressable keys in an order which you can access through their index
	#print(pygame.K_UP) #273 ie Up arrow key has an index of 273
	#print(pressed_keys[pygame.K_UP]) #So when you do pressed_keys[273] ,it shows that the Up arrow key is detected and nts a value of 1 when you hit the Up arrow key
	if pressed_keys[pygame.K_UP] == 1:    #if it detects Up arrow key being hit
		y-=5
        enemyIndex = 0
	for enemyImageX,enemyImageY,movingRight in enemyList:
		if enemyImageX >= 900-40:
			movingRight = False
		elif enemyImageX <= 5:
			movingRight = True
		if movingRight:
			enemyImageX+=(5*level) #with each level,the enemy's speed increases by a multiple of 5
		else:
			enemyImageX-=(5*level)
		#put the latest positions of the enemy back into the list
		enemyList[enemyIndex] = (enemyImageX,enemyImageY,movingRight)
		#move to the next index to update
		enemyIndex+=1
	#load the background image everytime so as to cover up the trail left behind by the movement of the player image
	screen.blit(backgroundImage,(0,0))
	#load the treasure image everytime
	screen.blit(treasureImage,(treasureImageX,treasureImageY))
	#load the player image everytime
	screen.blit(playerImage,(x,y))
	#load the enemy images everytime
	for enemyImageX,enemyImageY,movingRight in enemyList:
		screen.blit(enemyImage,(enemyImageX,enemyImageY))
	#check if the player and the treasure make a contact and store the outcome
	contactTreasure,y = checkContact(x,y,treasureImageX,treasureImageY)
	#check if the player and the enemy make a contact for each enemy
	for enemyImageX,enemyImageY,movingRight in enemyList:
		contactEnemy,y = checkContact(x,y,enemyImageX,enemyImageY)
	if contactTreasure: #if contact between the player and treasure happens
		#increase the level by one
		level+=1
		enemyList.append((enemyImageX-100*level,enemyImageY-170,movingRight))
		#define the text and text color
		textWin = font.render("Congrats!You reached level {}".format(level),True,(255,255,0)) #text,anti alias,textcolor
		#load up the text and display it
		screen.blit(textWin,(150,350))
		#update the screen with the text
		pygame.display.flip()
		#pause for 1 second (for the text to be visible longer)
		time.sleep(1)
	#update the display
	pygame.display.flip()
	frame.tick(30) #define a frame rate of 30fps ie the program is paused for 1/30th of a second
	if level>4:	
		#define a text for successful completion of the game
		textGameComplete = font.render("You completed the game successfully!",True,(255,255,255))
		#load up the text and display it
		screen.blit(textGameComplete,(80,500))
		#update the screen with the text
		pygame.display.flip()
		#pause for 1 second (for the text to be visible longer)
		time.sleep(1)
		finished = True #end the game
