import pygame
import random
import os
pygame.mixer.init()

pygame.init() 

#colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600

gameWindow = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

start_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(start_img, (screen_width, screen_height))

gameover_img = pygame.image.load("over.png")
gameover_img = pygame.transform.scale(gameover_img, (screen_width, screen_height)).convert_alpha()

eat_sound = pygame.mixer.Sound("eating.mp3")


gameWindow = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("SnakeWithVikas")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)  
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(start_img, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #pygame.mixer.music.load('back.mp3')   #sirf load kiya hai
                    #pygame.mixer.music.play()
                    gameLoop()    
        
        pygame.display.update()    
        clock.tick(60)

def gameLoop():
    exit_game = False
    game_over = False
    snake_x = 45 
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, int(screen_width/2))
    food_y = random.randint(20, int(screen_height/2))

    score = 0
    init_velociity = 5

    snake_size = 30 
    fps = 60

    while not exit_game:

        if game_over:

            gameWindow.blit(gameover_img, (0, 0))  # GAME OVER IMAGE
           

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # restart the game
                        game_over = False
                        snake_x = 45
                        snake_y = 55
                        velocity_x = 0
                        velocity_y = 0
                        snk_list = []
                        snk_length = 1
                        food_x = random.randint(20, int(screen_width/2))
                        food_y = random.randint(20, int(screen_height/2))
                        score = 0

            clock.tick(fps)
            continue

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velociity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velociity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velociity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velociity 
                        velocity_x = 0
                        
                    if event.key == pygame.K_q:
                        score += 10  

        snake_x += velocity_x
        snake_y += velocity_y

        if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:  
            score += 10
            eat_sound.play() 
            food_x = random.randint(20, screen_width/2)
            food_y = random.randint(20, screen_height/2) 
            snk_length += 5
            
            if score > int(highscore):
                highscore = score

        gameWindow.fill(white)
        gameWindow.blit(bgimg, (0, 0)) 
        text_screen("score: " + str(score) + "  highscore: " + str(highscore), red, 5, 5) 
        pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

        head = []
        head.append(snake_x)
        head.append(snake_y)
        snk_list.append(head)
        
        if len(snk_list) > snk_length:
            del snk_list[0]
            
        if head in snk_list[:-1]:
            game_over = True
            pygame.mixer.music.load('out.mp3')  #sirf load kiya hai
            pygame.mixer.music.play()    
            
        if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
            game_over = True    
            pygame.mixer.music.load('out.mp3')   #sirf load kiya hai
            pygame.mixer.music.play()

        plot_snake(gameWindow, (0, 255, 0), snk_list, snake_size)
        
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
