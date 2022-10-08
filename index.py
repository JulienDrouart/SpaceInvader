import os

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
        insert_query = "INSERT INTO score VALUES (" + str(score) + ")"
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

def loopFunction():
    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('SpaceInvader')

    run = True
    start = gameover = False
    fond = pygame.image.load("fond.jpg")
    rocket = pygame.image.load("rocket.png")
    screen.blit(fond, (0, 0))
    shipCooX = 500
    direction = "null"
    font = pygame.font.Font('freesansbold.ttf', 32)
    shipImg = pygame.image.load("ship.png")
    screen.blit(shipImg, (shipCooX, 730))
    score = rocketPosX = 0
    rocketPosY = 2000
    clock = pygame.time.Clock()
    shipSpeed = 9
    highscore = selectDatabase()
    text2 = font.render('Highest Score : ' + str(highscore), True, (255, 255, 255))
    screen.blit(text2, (700, 20))
    screen.blit(rocket, (rocketPosX, rocketPosY))
    beginText = font.render("Press any key to begin", True, (255, 255, 255))
    screen.blit(beginText, (350, 500))
    rocketState = "waiting"
    intervalOf10 = row = 0
    invaders = {}
    invaderImg = pygame.image.load("invader.png")

    for i in range(70):
        invaders[i] = {'posX': (intervalOf10 * 100)+25, 'posY': (row * 50)+100, 'state': "alive"}
        screen.blit(invaderImg, ((intervalOf10 * 100)+25, (row * 50)+100))

        if intervalOf10 < 9:
            intervalOf10 += 1
        else:
            intervalOf10 = 0
            row += 1

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
                        loopFunction()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if start is False:
                        timerEverySeconds = time.time()
                        start = True
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                    if event.key == pygame.K_RIGHT:
                        direction = "right"
                    if event.key == pygame.K_SPACE and rocketState == "waiting":
                        rocketPosX = shipCooX + 25
                        rocketPosY = 750
                        rocketState = "launching"
                if event.type == pygame.KEYUP:
                    direction = "null"
            if rocketState == "launching":
                if rocketPosY < -50:
                    rocketState = "waiting"
                else:
                    rocketPosY -= 6
            if direction == "left":
                if shipCooX < 10:
                    shipCooX = shipCooX
                else:
                    shipCooX = shipCooX - shipSpeed
            if direction == "right":
                if shipCooX > 940:
                    shipCooX = shipCooX
                else:
                    shipCooX = shipCooX + shipSpeed

            if start is True:
                screen.blit(fond, (0, 0))
                img = font.render('Score : ' + str(score), True, (255, 255, 255))
                scoreText = font.render('Highest Score : ' + str(highscore), True, (255, 255, 255))
                screen.blit(shipImg, (shipCooX, 730))
                screen.blit(rocket, (rocketPosX, rocketPosY))
                screen.blit(img, (20, 20))
                screen.blit(scoreText, (700, 20))
                for i in range(70):
                    screen.blit(invaderImg, (invaders[i]["posX"],invaders[i]["posY"]))
                    invaders[i]["posY"]+=3
                    if invaders[i]["posY"] > 730:
                        gameover = True


        clock.tick(60)
        pygame.display.flip()

loopFunction()
