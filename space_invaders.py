"""
    rajouter les fonctionnalités suivantes :
- l'initialisation des ennemis
- le déplacement des ennemis vers le bas de l'écran ou sur les côtés
- la capacité de pouvoir tirer pour le joueur
- la gestion des collisions
- plus tout autre bonus que vous jugerez adéquat !

Bon courage !
"""

import turtle
import time
import random


# Initialisation de la fenêtre
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)  # Désactive l'animation automatique pour un rendu fluide

TOP = window.window_height() / 2
RIGHT = window.window_width() / 2
BOTTOM = window.window_height() / 2
LEFT = window.window_width() / 2
GUTTER = 0.025 * window.window_width()

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

# Initialisation du vaisseau du joueur
player = turtle.Turtle()
player.speed(0)
player.shape("triangle")
player.color("orange")
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation des projectiles
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.3, stretch_len=0.3)
bullet.penup()
bullet.hideturtle()

# Initialisation des ennemis
Ennemies = []
for i in range(5):
    ennemies = turtle.Turtle()
    ennemies.speed(0)
    ennemies.shape("triangle")
    ennemies.color("red")
    ennemies.penup()
    ennemies.goto(0, 250)
    ennemies.setheading(90)


def create_ennemies():
    Ennemie = turtle.Turtle()
    Ennemie.penup()
    Ennemie.turtlesize(1.5)
    (
        Ennemie.setposition(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    Ennemie.shape("turtle")
    Ennemie.setheading(-90)
    Ennemie.color(random.random(), random.random(), random.random())
    Ennemies.append(Ennemie)


lasers = []


# Fonctions de déplacement
def move_left():
    x = player.xcor()
    if x > -380:
        player.setx(x - 20)


def move_right():
    x = player.xcor()
    if x < 380:
        player.setx(x + 20)


LASER_LENGHT = 20
LASER_SPEED = 10
ALIEN_SPAWN_INTERVAL = 1.2


def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1, 0, 0)
    laser.hideturtle()
    laser.setposition(player.xcor(), player.ycor())
    laser.setheading(90)
    laser.forward(20)
    laser.pendown()
    laser.pensize(5)

    lasers.append(laser)


def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    laser.forward(LASER_LENGHT)
    laser.forward(LASER_LENGHT)
    laser.forward(LASER_LENGHT)


# Ennemies moves
def enmove_left():
    x = ennemies.xcor()
    if x < 360:
        ennemies.setx(x + 20)


def enmove_right():
    x = ennemies.ycor
    if x < -360:
        ennemies.ycor(x + 70)


# Écoute des touches
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(create_laser, "space")

alien_timer = 0
# Boucle de jeu
while lives > 0:
    window.update()
    time.sleep(0.05)  # Ralentit la boucle

    # Gestion des tirs
    for laser in lasers:
        move_laser(laser)
        if laser.ycor() > TOP:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)
            turtle.turtles().remove(laser)
    window.update()

    # Déplacement des ennemis

    # Collion lasers et ennemies
    for ennemie in ennemies:
        # on vérie si le laser est proche de l'énnemie
        if lasers.distance(ennemie) < 20:
            print("Touché")
            ennemie.hideturtle()
            ennemie.goto(1000, 1000)

    # Détection des collisions


# Affichage de l'écran de victoire
if lives == 0:
    score_display.goto(0, 0)
    score_display.write("GAME OVER", align="center", font=("Courier", 24, "normal"))
else:
    score_display.goto(0, 0)
    score_display.write("GG WP !", align="center", font=("Courier", 24, "normal"))

window.mainloop()
