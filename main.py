import pygame
import random
import os

pygame.init()

display_width = 800
display_height = 600

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,100)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

white = (255, 255, 255)
black = (0, 0, 0)
grey = (122, 122, 122)
red = (255, 0, 0)
light_red = (255,153,153)
green = (0, 204, 102)
light_green = (204, 255, 153)
blue = (0,0,255)
light_blue = (153, 153, 255)
yellow = (252,237,66)
light_yellow = (255, 255, 178)

img = pygame.image.load('snakeHead.png')
appleimg = pygame.image.load('apple.png')
rockimg = pygame.image.load('rock.png')

appleBite = pygame.mixer.Sound("AppleBite.wav")
snakeCrash = pygame.mixer.Sound("Smashing.wav")

pygame.mixer.music.load("background.mp3")

clock = pygame.time.Clock()

AppleThickness = 30
block_size = 20
FPS = 10

direction = "right"

extrasmallfont = pygame.font.SysFont("comicsansms", 15)
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 65)


def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    text2 = extrasmallfont.render("P : Pause ", True, grey)
    text3 = extrasmallfont.render("^ : Up ", True, grey)
    text4 = extrasmallfont.render("> : Right ", True, grey)
    text5 = extrasmallfont.render("< : Left ", True, grey)
    text6 = extrasmallfont.render("v : Down ", True, grey)
    gameDisplay.blit(text, [0,0])
    gameDisplay.blit(text2, [5,500])
    gameDisplay.blit(text3, [5,520])
    gameDisplay.blit(text4, [5,540])
    gameDisplay.blit(text5, [5,560])
    gameDisplay.blit(text6, [5,580])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))
    randAppleY = round(random.randrange(0, display_height - AppleThickness))

    return randAppleX, randAppleY

def randRockGen():
    randRockX = round(random.randrange(0, display_width - AppleThickness))
    randRockY = round(random.randrange(0, display_height - AppleThickness))

    return randRockX, randRockY

def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, color, size):
    if size == "extrasmall":
        textSurface = extrasmallfont.render(text, True, color)
    elif size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, butonheight, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx+(buttonwidth/2), buttony+(butonheight/2)))
    gameDisplay.blit(textSurf, textRect)

def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "easy":
                gameLoop(10)
            if action == "medium":
                gameLoop(15)
            if action == "hard":
                gameLoop(20)
            if action == "record":
                records()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)

def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def game_intro():
    intro = True
    pygame.mixer.music.play(-1)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Snake Game", green, -150, "large")
        message_to_screen("The objective of the game is to eat apples.", black, -90, "small")
        message_to_screen("More apples you eat, longer you get.", black, -50, "small")
        message_to_screen("Choose your level", black, 110, "small")

        button("Records", 350,310,100,50, yellow, light_yellow, action="record")
        button("Easy", 150,450,100,50, blue, light_blue, action="easy" )
        button("Medium", 350,450,100,50, green, light_green, action="medium")
        button("Hard", 550,450,100,50, red, light_red, action="hard" )

        pygame.display.update()
        clock.tick(FPS)

def records():
    record = True
    file = open('scores.txt')
    lines = sorted(file.readlines(), reverse = True, key = int)
    while record:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_intro()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Records", green, -210, "large")
        message_to_screen("Top 10 Records", green, -160, "extrasmall")

        lineHeight = -130
        i = 0
        for line in lines:
            line = line[:-1]
            message_to_screen(str(i + 1) + "°: " + str(line), black, lineHeight, "small")
            lineHeight += 30
            i += 1
            if i == 10:
                break
        file.close()

        message_to_screen("Press R to return to the main menu", black, 210, "small")

        pygame.display.update()
        clock.tick(FPS)

def pause():
    paused = True
    gameDisplay.fill(white)
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press R to return to the main menu", black, 0)
    message_to_screen("Press C to continue", black, 30)
    message_to_screen("Press Q to quit", black, 60)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_r:
                    game_intro()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(FPS)

def gameLoop(FPS):
    global direction
    global highestScore

    highestScore = 0
    file = open('scores.txt')
    for line in file:
        if int(line) > int(highestScore):
            highestScore = line
    file.close()

    direction = "right"
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_chain = 20
    lead_y_chain = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()
    randRockX, randRockY = randRockGen()
    randRockX2, randRockY2 = randRockGen()
    randRockX3, randRockY3 = randRockGen()

    while not gameExit:
        pygame.mixer.music.stop()

        if gameOver == True:
            f = open('scores.txt', 'a')
            f.writelines(str(snakeLength-1) + "\n")
            f.close()

        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over", red, -120, size="large")
            message_to_screen("Press R to return to the main menu", black, -50, size="small")
            message_to_screen("Press C to play again", black, -20, size="small")
            message_to_screen("Press Q to quit", black, 10, size="small")
            if (snakeLength - 1) > int(highestScore):
                message_to_screen("New Highest Score! Contratulations!!", green, 50, size="extrasmall")
            message_to_screen("Your Score: " + str(snakeLength-1), black, 80, size="small")
            message_to_screen("Highest Score: " + highestScore[:-1], black, 110, size="small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_r:
                        game_intro()
                    if event.key == pygame.K_c:
                        gameLoop(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    lead_x_chain = - block_size
                    lead_y_chain = 0
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    lead_x_chain = + block_size
                    lead_y_chain = 0
                elif event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    lead_y_chain = - block_size
                    lead_x_chain = 0
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    lead_y_chain = + block_size
                    lead_x_chain = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x > display_width - block_size or lead_x < 0 or lead_y > display_height - block_size or lead_y < 0:
            gameOver = True

        lead_x += lead_x_chain
        lead_y += lead_y_chain
        gameDisplay.fill(white)

        gameDisplay.blit(rockimg, (randRockX, randRockY))
        if randRockX > randAppleX and randRockX < randAppleX + AppleThickness or randRockX + AppleThickness > randAppleX and randRockX + AppleThickness < randAppleX + AppleThickness:
            if randRockY > randAppleY and randRockY < randAppleY + AppleThickness or randRockY + AppleThickness > randAppleY and randRockY + AppleThickness < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()

        if FPS == 15 or FPS == 20:
            gameDisplay.blit(rockimg, (randRockX2, randRockY2))
            if randRockX2 > randAppleX and randRockX2 < randAppleX + AppleThickness or randRockX2 + AppleThickness > randAppleX and randRockX2 + AppleThickness < randAppleX + AppleThickness:
                if randRockY2 > randAppleY and randRockY2 < randAppleY + AppleThickness or randRockY2 + AppleThickness > randAppleY and randRockY2 + AppleThickness < randAppleY + AppleThickness:
                    randAppleX, randAppleY = randAppleGen()

        if FPS == 20:
            gameDisplay.blit(rockimg, (randRockX3, randRockY3))
            if randRockX3 > randAppleX and randRockX3 < randAppleX + AppleThickness or randRockX3 + AppleThickness > randAppleX and randRockX3 + AppleThickness < randAppleX + AppleThickness:
                if randRockY3 > randAppleY and randRockY3 < randAppleY + AppleThickness or randRockY3 + AppleThickness > randAppleY and randRockY3 + AppleThickness < randAppleY + AppleThickness:
                    randAppleX, randAppleY = randAppleGen()

        gameDisplay.blit(appleimg, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score(snakeLength-1)

        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
                pygame.mixer.Sound.play(appleBite)

        if lead_x > randRockX and lead_x < randRockX + AppleThickness or lead_x + block_size > randRockX and lead_x + block_size < randRockX + AppleThickness:
            if lead_y > randRockY and lead_y < randRockY + AppleThickness or lead_y + block_size > randRockY and lead_y + block_size < randRockY + AppleThickness:
                pygame.mixer.Sound.play(snakeCrash)
                gameOver = True

        if FPS == 15 or FPS == 20:
            if lead_x > randRockX2 and lead_x < randRockX2 + AppleThickness or lead_x + block_size > randRockX2 and lead_x + block_size < randRockX2 + AppleThickness:
                if lead_y > randRockY2 and lead_y < randRockY2 + AppleThickness or lead_y + block_size > randRockY2 and lead_y + block_size < randRockY2 + AppleThickness:
                    pygame.mixer.Sound.play(snakeCrash)
                    gameOver = True

        if FPS == 20:
            if lead_x > randRockX3 and lead_x < randRockX3 + AppleThickness or lead_x + block_size > randRockX3 and lead_x + block_size < randRockX3 + AppleThickness:
                if lead_y > randRockY3 and lead_y < randRockY3 + AppleThickness or lead_y + block_size > randRockY3 and lead_y + block_size < randRockY3 + AppleThickness:
                    pygame.mixer.Sound.play(snakeCrash)
                    gameOver = True

        clock.tick(FPS)

    pygame.quit()
    quit()
game_intro()
gameLoop()