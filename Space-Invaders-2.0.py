# J'ai demandé à claude de faire une correction de ce qui ne marche pas

import turtle
import time
import random
import pygame


# Initialisation de la fenêtre
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)

TOP = window.window_height() / 2
RIGHT = window.window_width() / 2
BOTTOM = -(window.window_height() / 2)  # BUG 1 : était positif, doit être négatif
LEFT = -(window.window_width() / 2)      # BUG 2 : idem pour LEFT
GUTTER = 0.025 * window.window_width()

# Initialisation de la musique du jeu et des effets
pygame.mixer.init()
pygame.mixer.music.load("moodmode-that-8-bit-music-322062.mp3")  # on ajoute la musique de fond
pygame.mixer.music.set_volume(0.5)      # volume entre 0.0 et 1.0
pygame.mixer.music.play(-1)

son_laser = pygame.mixer.Sound("driken5482-retro-laser-1-236669.mp3") # on défini le son des laser
son_explosion = pygame.mixer.Sound("0bl1v10n-heavy-footstep-372974.mp3") # on défini le son des explosions lors dela


# Affichage du score et des vies
score = 0
lives = 3
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)
score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "normal"))

def update_score():
    score_display.clear()
    score_display.goto(-380, 260)
    score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "normal"))

# Initialisation du vaisseau du joueur
player = turtle.Turtle()
player.speed(0)
player.shape("triangle")
player.color("orange")
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation des projectiles
lasers = []

LASER_LENGTH = 20
LASER_SPEED = 15 # j'augmente la vitesse du lasers

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("yellow")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.3, stretch_len=1)
    laser.setposition(player.xcor(), player.ycor() + 20)
    laser.setheading(90)
    lasers.append(laser)
    son_laser.play() # on ajoute le son du laser

def move_laser(laser):
    laser.forward(LASER_SPEED)

# Initialisation des ennemis
Ennemies = []
ALIEN_SPAWN_INTERVAL = 1.2
alien_timer = 0

def create_ennemy():
    # BUG 3 : setposition mal appelée (virgule dans les parenthèses, tuple invalide)
    ennemy = turtle.Turtle()
    ennemy.penup()
    ennemy.turtlesize(1.5)
    x = random.randint(int(LEFT + GUTTER), int(RIGHT - GUTTER))
    ennemy.setposition(x, TOP - GUTTER)
    ennemy.shape("turtle")
    ennemy.setheading(-90)
    ennemy.color(random.random(), random.random(), random.random())
    # Vitesse de déplacement aléatoire
    ennemy.speed_val = random.uniform(1.5, 3.5)
    Ennemies.append(ennemy)

# Pré-spawn de quelques ennemis
for _ in range(5):
    create_ennemy()

# Fonctions de déplacement du joueur
def move_left():
    x = player.xcor()
    if x > LEFT + 10:
        player.setx(x - 50) # j'augmente la vitesse vers la gauche

def move_right():
    x = player.xcor()
    if x < RIGHT - 10:
        player.setx(x + 50)# j'augmente la vitesse vers la droite

# Écoute des touches
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(create_laser, "space")

# Boucle de jeu
while lives > 0:
    window.update()
    time.sleep(0.03)

    alien_timer += 0.03
    if alien_timer >= ALIEN_SPAWN_INTERVAL:
        alien_timer = 0
        create_ennemy()

    # Déplacement des lasers
    for laser in lasers[:]:
        move_laser(laser)
        if laser.ycor() > TOP:
            laser.hideturtle()
            laser.clear()
            lasers.remove(laser)

    # Déplacement des ennemis vers le bas
    # BUG 4 : enmove_left/right utilisaient xcor/ycor de manière incorrecte,
    #          et itéraient sur une variable non définie. Remplacé par une logique directe.
    for ennemy in Ennemies[:]:
        ennemy.forward(ennemy.speed_val)

        # Si l'ennemi atteint le bas → le joueur perd une vie
        if ennemy.ycor() < BOTTOM + 10:
            ennemy.hideturtle()
            Ennemies.remove(ennemy)
            lives -= 1
            update_score()
            continue

        # BUG 5 : lasers.distance() appelé sur la liste au lieu de chaque laser
        # Collision laser <-> ennemi
        for laser in lasers[:]:
            if laser.distance(ennemy) < 20:
                # Touché !
                ennemy.hideturtle()
                Ennemies.remove(ennemy)
                laser.hideturtle()
                lasers.remove(laser)
                score += 10
                update_score()
                break

        # Collision ennemi <-> joueur
        if ennemy.distance(player) < 25:
            ennemy.hideturtle()
            Ennemies.remove(ennemy)
            lives -= 1
            update_score()
            son_explosion.play() # on ajoute la musique des explosions

    # Victoire si tous les ennemis sont éliminés et aucun ne respawn
    # (ici on joue indéfiniment jusqu'à 0 vie)

window.update()

# Affichage de l'écran de fin
score_display.goto(0, 0)
if score > 0:
    score_display.write("GAME OVER", align="center", font=("Courier", 24, "normal"))
else:
    score_display.write("GAME OVER", align="center", font=("Courier", 24, "normal"))

window.mainloop()