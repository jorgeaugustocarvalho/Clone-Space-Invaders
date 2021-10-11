import pygame
from pygame import mixer
import random
from math import pow, sqrt

pygame.init()

print(pygame.font.get_fonts())

# tela 
screen = pygame.display.set_mode((500, 500))
# nome do game la em cima
pygame.display.set_caption("SpaceInvadersByJorgin")
# icon do game la em cima
icon = pygame.image.load("images/spaceship.png")
pygame.display.set_icon(icon)

#mixer.music.load("")
#mixer.music.play(-1) # -1 faz tocar música em loop

#background

background = pygame.image.load("images/background.jpg")

# player
player_1 = pygame.image.load("images/spaceship.png")
player_x = 240
player_y = 443
player_vel = 0.1
player_movement_x = 0

# display de pontos
score_value = 0

font = pygame.font.Font("freesansbold.ttf", 20)

txt_x = 10
txt_y = 10

# game over text

over =  pygame.font.Font("freesansbold.ttf", 64)

def game_over():
    gameOver = over.render("GAME OVER", True, (0, 255, 0))
    screen.blit(gameOver, (50, 140))

def text(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


#player function
def player(x, y):
    screen.blit(player_1, (x, y))

#enemy

# adendo: para criar e controlar um numero de inimigos foram utilizadas listas
enemy_1 = []
enemy_x = []
enemy_y = []
enemy_movement_x = []
enemy_movement_y = []

num_enemies = 15

for i in range(num_enemies):

    enemy_1.append(pygame.image.load("images/alienzito.png"))
    enemy_x.append(random.randint(0, 468))
    enemy_y.append(random.randint(0, 150))
    enemy_movement_x.append(0.3)
    enemy_movement_y.append(20)

#enemy function
def enemy(x, y, i):
    screen.blit(enemy_1[i], (x, y))

# bullet

bullet = pygame.image.load("images/tiro.png") 
bullet_x = 0
bullet_y = 440
bullet_movement_x = 0
bullet_movement_y = 0.5
bullet_state = "ready" # ready state significa que vc não pode ver o tiro na tela e "fire" o tiro está acontecendo

# bullets function
def bullets(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x, y)) # tiro saindo de cima do player o + 16 e o +10 são pra isso

# collision function

def isCollision(x1, y1, x2, y2):
    distance = sqrt((pow(x2 - x1, 2)) + (pow(y2 - y1, 2)))
    if distance < 13:
        return True
    else:
        return False

#velocidade do player
velol = 0.2

#velocidade do inimigo


loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.KEYDOWN: # condição pra ver se usuário pressiona botão
            if event.key == pygame.K_LEFT:
                player_movement_x = -velol
            if event.key == pygame.K_RIGHT:
                player_movement_x = velol
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready": # condicional para que ele atire denovo
                    bullet_x = player_x # guardamos o valor de player_x em bullet_x uma variavel estática para o tiro não seguir a trajetória do player
                    bullets(bullet_x, bullet_y)

        if event.type == pygame.KEYUP: # condição quando o usuário solta o botão (para parar)
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_movement_x = 0


    screen.fill((0, 255, 0))
    
    #colocando background
    screen.blit(background,(0,0))
    
    # movimento do player1
    player_x += player_movement_x

    
    # tiro do player

    if bullet_state == "fire":
        bullets(bullet_x, bullet_y) #colocamos a variavel bullet_x aqui também
        bullet_y -= bullet_movement_y

    #múltiplos tiros

    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = 430

    #criando invisible wall do player
    if player_x <= 0:
        player_x = 0
    elif player_x >= 468:
        player_x = 468

    

    
    #criando invisible wall do inimigo
    # aqui é diferente utilizamos a barreira para fazer o inimigo se movimentar , bater na parede e voltar
    for i in range(num_enemies):
        
        if enemy_y[i] > 430:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        enemy_x[i] += enemy_movement_x[i]
        if enemy_x[i] <= 2:
            enemy_movement_x[i] = 0.3
            enemy_y[i] += enemy_movement_y[i]
        elif enemy_x[i] >= 468:
            enemy_movement_x[i] = - 0.3
            enemy_y[i] += enemy_movement_y[i]

        # game over
    
        #collision

        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
    
        if collision: # se a colisão acontecer volta ao estado original do tiro como no if bullet_y <= 0
            bullet_state = "ready"
            bullet_y = 450
            score_value += 1
            enemy_x[i] = random.randint(0, 468)
            enemy_y[i] = random.randint(0, 150)
        
        
        enemy(enemy_x[i], enemy_y[i], i)

    player(player_x , player_y)

    #score

    text(txt_x, txt_y)
    
    pygame.display.update()
