import pygame, sys
import random
import time
import sqlite3
from pygame.locals import *
from sqlite3 import Error

connection = sqlite3.connect('score.db')
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS score (highscore int)"
cursor.execute(create_table)

def insertDatabase(score):
    dbHighestScore = selectDatabase()
    if score > dbHighestScore:
        # create table in database
        insert_query = "INSERT INTO score VALUES ("+str(score)+")"
        cursor.execute(insert_query)
        connection.commit()

def selectDatabase():
    result = 0
    select_query = "SELECT MAX(highscore) FROM score"
    cursor.execute(select_query)
    result = cursor.fetchone()
    highScore = result[0]
    if str(highScore) == 'None':
        highScore = 0
    return highScore

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('SpaceInvader')

run = True
start = gameover = False
shipCooX = 260
direction = "null"
font = pygame.font.Font('freesansbold.ttf', 32)
shipImg = pygame.image.load("ship.png")
score = 0
clock = pygame.time.Clock()
shipSpeed = 7
highscore = selectDatabase()
screen.fill((0, 0, 0))
img = font.render('Score : ' + str(score), True, (255, 255, 255))
text2 = font.render('Highest Score : ' + str(highscore), True, (255, 255, 255))
screen.blit(shipImg, (shipCooX, 730))
screen.blit(img, (20, 20))
screen.blit(text2, (800, 20))

while run:

    while gameover:
        font = pygame.font.SysFont(None, 50)
        end = font.render('Press Enter to restart game', True, (255, 255, 255))
        screen.blit(end, (50, 50))
        clock.tick(60)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                insertDatabase(score)
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    insertDatabase(score)
                    screen = pygame.display.set_mode((1000, 800))
                    run = True
                    start = gameover = False
                    font = pygame.font.SysFont(None, 24)
                    clock.tick(60)
                    highscore = selectDatabase()
                    pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if start is False:
                    timerEverySeconds = time.time()
                    start = True
                if event.key == pygame.K_LEFT:
                    shipCooX = shipCooX - shipSpeed
                    if shipCooX < 0:
                        shipCooX = shipCooX
                if event.key == pygame.K_RIGHT:
                    shipCooX = shipCooX + shipSpeed
                    if shipCooX > 970:
                        shipCooX = shipCooX

        if start is True:
            screen.fill((0, 0, 0))
            img = font.render('Score : ' + str(score), True, (255, 255, 255))
            text2 = font.render('Highest Score : ' + str(highscore), True, (255, 255, 255))
            screen.blit(shipImg, (shipCooX, 730))
            screen.blit(img, (20, 20))
            screen.blit(text2, (800, 20))

    clock.tick(60)
    pygame.display.flip()