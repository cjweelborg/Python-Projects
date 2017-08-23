import pygame
import time
import random

#Initialization of pygame
pygame.init()

#Initialize colors and variables

#Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Display width and height
displayWidth = 1280
displayHeight = 720

#Frames Per Second
FPS = 60

#Movement in pixels
PlayerSpeed = 1

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Pythopede')



clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)



def message_to_screen(msg,color,x,y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x,y])



def gameLoop():
    #Define variables
    running = True
    inGame = True
    lead_x = displayWidth/2
    lead_y = displayHeight/2
    lead_x_change = 0
    lead_y_change = 0
    playerSize = 10
    foodSize = 10

    randFoodX = random.randrange(0, displayWidth-foodSize)
    randFoodY = random.randrange(0, displayHeight-foodSize)
    
    #Basic game loop
    while running:

        while inGame == False:
            gameDisplay.fill(black)
            message_to_screen("Game over, press C to play again or Q to quit",red,displayWidth/2,displayHeight/2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        #Set inGame to true to get out of the loop, then exit the game
                        inGame = True
                        running = False
                    if event.key == pygame.K_c:
                        gameLoop()
        #Event Handling
        for event in pygame.event.get():
            #Quit event
            if event.type == pygame.QUIT:
                running = False
            #Check Key Down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = PlayerSpeed * -1
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = PlayerSpeed
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = PlayerSpeed * -1
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = PlayerSpeed 
                    lead_x_change = 0

            #Check Key Up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    lead_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    lead_y_change = 0

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x >= displayWidth or lead_x < 0 or lead_y >= displayHeight or lead_y < 0:
            inGame = False
        
        gameDisplay.fill(black)
        food = pygame.draw.rect(gameDisplay, green,[randFoodX,randFoodY,foodSize,foodSize])
        player = pygame.draw.rect(gameDisplay, red, [lead_x,lead_y,playerSize,playerSize])
        
        #Update the display
        pygame.display.update()

        #Check for collision
        if( (lead_x >= randFoodX and lead_x <= (randFoodX + foodSize)) or ((lead_x + playerSize) >= randFoodX and (lead_x + playerSize) <= (randFoodX + foodSize)) ):
            if( (lead_y >= randFoodY and lead_y <= (randFoodY + foodSize)) or ((lead_y + playerSize) >= randFoodY and (lead_y + playerSize) <= (randFoodY + foodSize)) ):
                print("collision")

        clock.tick(FPS)
        
    #Quit the program
    pygame.quit()
    quit()

gameLoop()
