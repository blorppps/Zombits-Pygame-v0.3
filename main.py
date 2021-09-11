#setup
'START BLOCK'
import pygame
import keyboard
import math

from sprites import *
from map import *

pygame.init()

screen = pygame.display.set_mode((1200,600))

running = True

clock = pygame.time.Clock()

font = pygame.font.Font(None,32)
'END BLOCK'

#environment
'START BLOCK'
groundshift = 0

#should only be used for rendering, not collisions or anything else
#IMPORTANT - THIS IS LITERALLY USED TO RENDER EVERYTHING IN THE ENTIRE GAME
camX = 600
#literally used for nothing
camY = 0

time = 0
day = 1
daycolor = (200,200,250)

difficulty = 1

weaponicons = {'arrows':arrowicon,'bow':bow,'morningstar':morningstar,'boomerang':boomerang}
'END BLOCK'

#players
'START BLOCK'
class player1:
    X = 0
    Y = 455

    direction = 'left'
    move = 'none'

    weaponswitch = True
    weapon = 'sword'

    currenthouse = 'none'

    class sword:
        sprite = sword
        
        sword = 0
        length = 0
        state = 'none'

        rect = sprite.get_rect()

    class bow:
        pull = 0
        timer = 0

    class boomerang:
        position = (0,0)
        speed = 0
        direction = 'none'
        rotation = 0
        thrown = False
        cooldown = 0

        rect = boomerang.get_rect()

    sprite = p1
    rect = sprite.get_rect()
    rect.topleft = (X,Y)

class player2:
    X = 0
    Y = 455

    direction = 'left'
    move = 'none'

    weaponswitch = True
    weapon = 'sword'

    currenthouse = 'none'

    class sword:
        sprite = sword
        
        sword = 0
        length = 0
        state = 'none'

        rect = sprite.get_rect()

    class bow:
        pull = 0
        timer = 0

    class boomerang:
        position = (0,0)
        speed = 0
        direction = 'none'
        rotation = 0
        thrown = False
        cooldown = 0

        rect = boomerang.get_rect()
        
    sprite = p2
    rect = sprite.get_rect()
    rect.topleft = (X,Y)

screenX = 0

bothmoving = False

speed = 3

health = 100
arrows = 10

unlockedweapons = ['sword']
'END BLOCK'

#enemies
'START BLOCK'
enemies = []

enemytimer = 500
'END BLOCK'

#projectiles
'START BLOCK'
projectiledata = []
'END BLOCK'

#main loop
while running:

    #quit
    'START BLOCK'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    'END BLOCK'

    #environment
    'START BLOCK'
    #sky
    screen.fill(daycolor)

    time = time + 0.2

    #sunrise
    if time > 0 and time < 200:
        daycolor = (0+time,0+time,50+time)
    #day
    if time > 200 and time < 1000:
        daycolor = (200,200,250)
    #sunset
    if time > 1000 and time < 1200:
        daycolor = (200-time+1000,200-time+1000,250-time+1000)
    #night
    if time > 1200 and time < 2000:
        daycolor = (0,0,50)
    if time > 2000:
        time = 0
        day = day + 1
        difficulty = difficulty + 0.1

    #ground
    for i in range (17):
        if bothmoving:
            groundshift = camX%80
        screen.blit(ground,(-80+i*80+groundshift,camY+500))

    #houses
    for housedata in houses:

        #entering houses
        doorrect = door.get_rect()
        doorrect.topleft = housedata['doorposition']

        if doorrect.colliderect(player1.rect):
            if keyboard.is_pressed('w') and player1.weaponswitch:
                #going in
                if not housedata['entered'] and player2.currenthouse == 'none': #makes it so only one player at a time can enter houses
                    housedata['entered'] = True
                    player1.currenthouse = housedata['id']
                    player1.sprite.set_alpha(128)
                #going out
                elif housedata['entered']:
                    if not player2.currenthouse == housedata['id']:
                        housedata['entered'] = False
                    player1.currenthouse = 'none'
                    player1.sprite.set_alpha(256)
                player1.weaponswitch = False

        if doorrect.colliderect(player2.rect):
            if keyboard.is_pressed('up') and player2.weaponswitch:
                #going in
                if not housedata['entered'] and player1.currenthouse == 'none':
                    housedata['entered'] = True
                    player2.currenthouse = housedata['id']
                    player2.sprite.set_alpha(128)
                #going out
                elif housedata['entered']:
                    if not player1.currenthouse == housedata['id']:
                        housedata['entered'] = False
                    player2.currenthouse = 'none'
                    player2.sprite.set_alpha(256)
                player2.weaponswitch = False

        #actually draw the house and door
        if housedata['entered']:
            screen.blit(houseentered,(camX+housedata['position'][0],camY+housedata['position'][1]))
            for item in housedata['contents']:
                screen.blit(weaponicons[item['weapon']],(camX+item['position'][0],camY+item['position'][1]))
                #buy weapons
                itemrect = weaponicons[item['weapon']].get_rect()
                itemrect.topleft = item['position']
                #normal weapons
                if (itemrect.colliderect(player1.rect) and keyboard.is_pressed('w')) or (itemrect.colliderect(player2.rect) and keyboard.is_pressed('up')):
                    if item['weapon'] == 'arrows':
                        pass
                    elif item['weapon'] == 'morningstar':
                        #star of the morning is seperate from normal weapons because it replaces the iron sword
                        unlockedweapons.remove('sword')
                        unlockedweapons.insert(0,'morningstar')
                        housedata['contents'].pop(housedata['contents'].index(item))
                        #update the sword
                        player1.sword.sprite = morningstar
                        player2.sword.sprite = morningstar
                        player1.weaponswitch = False
                        player2.weaponswitch = False
                    else:
                        unlockedweapons.append(item['weapon'])
                        housedata['contents'].pop(housedata['contents'].index(item))
                        player1.weaponswitch = False
                        player2.weaponswitch = False
                #buy arrows
                if itemrect.colliderect(player1.rect) and keyboard.is_pressed('w') and player1.weaponswitch:
                    if item['weapon'] == 'arrows' and 'bow' in unlockedweapons:
                        arrows = arrows + 10
                        player1.weaponswitch = False
                if itemrect.colliderect(player2.rect) and keyboard.is_pressed('up') and player2.weaponswitch:
                    if item['weapon'] == 'arrows' and 'bow' in unlockedweapons:
                        arrows = arrows + 10
                        player2.weaponswitch = False
                    
        else:
            screen.blit(house,(camX+housedata['position'][0],camY+housedata['position'][1]))
        screen.blit(door,(camX+housedata['doorposition'][0],camY+housedata['doorposition'][1]))

    #grass
    for grass in grassdata:
        if camX+grass['X'] > -100 and camX+grass['X'] < 1300:
            if grass['type'] == 0:
                grasssprite = grass1
            if grass['type'] == 1:
                grasssprite = grass2
            screen.blit(grasssprite,(camX+grass['X'],camY+490))
    'END BLOCK'

    #die
    'START BLOCK'
    if health <= 0:
        running = False
    'END BLOCK'

    #movement
    'START BLOCK'
    #p1
    a = keyboard.is_pressed('a')
    d = keyboard.is_pressed('d')

    #p2
    left = keyboard.is_pressed('left')
    right = keyboard.is_pressed('right')

    #p1
    if a != d:
        if a:
            player1.X = player1.X - speed
            player1.move = 'left'
            player1.direction = 'left'
        if d:
            player1.X = player1.X + speed
            player1.move = 'right'
            player1.direction = 'right'

    else:
        player1.move = 'none'

    #p2
    if left != right:
        if left:
            player2.X = player2.X - speed
            player2.direction = 'left'
            player2.move = 'left'
        if right:
            player2.X = player2.X + speed
            player2.move = 'right'
            player2.direction = 'right'
            
    else:
        player2.move = 'none'

    #makes it so the player cant leave the screen
    if camX+player1.X < 50:
        player1.X = 50 - camX
    if camX+player1.X > 1130:
        player1.X = 1130 - camX

    if camX+player2.X < 50:
        player2.X = 50 - camX
    if camX+player2.X > 1130:
        player2.X = 1130 - camX

    #makes it so the player cant walk through houses when inside
    if not player1.currenthouse == 'none':
        if player1.X < houses[player1.currenthouse]['position'][0]+5:
            player1.X = houses[player1.currenthouse]['position'][0]+5
        if player1.X > houses[player1.currenthouse]['position'][0]+250-25:
            player1.X = houses[player1.currenthouse]['position'][0]+250-25

    if not player2.currenthouse == 'none':
        if player2.X < houses[player2.currenthouse]['position'][0]+5:
            player2.X = houses[player2.currenthouse]['position'][0]+5
        if player2.X > houses[player2.currenthouse]['position'][0]+250-25:
            player2.X = houses[player2.currenthouse]['position'][0]+250-25

    #rect used for collisions
    player1.rect = player1.sprite.get_rect()
    player1.rect.topleft = (player1.X,player1.Y)

    player2.rect = player2.sprite.get_rect()
    player2.rect.topleft = (player2.X,player2.Y)

    #camera
    if player1.move == player2.move and player1.currenthouse == 'none' and player2.currenthouse == 'none':
        if player1.move == 'left':
            camX = camX + 3
        if player1.move == 'right':
            camX = camX - 3

        if not player1.move == 'none':
            bothmoving = True

    if player1.direction == 'right':
        screen.blit(pygame.transform.scale(player1.sprite,(20,45)),(camX+player1.X,camY+player1.Y))
    if player1.direction == 'left':
        screen.blit(pygame.transform.flip(pygame.transform.scale(player1.sprite,(20,45)),True,False),(camX+player1.X,camY+player1.Y))
    if player2.direction == 'right':
        screen.blit(pygame.transform.scale(player2.sprite,(20,45)),(camX+player2.X,camY+player2.Y))
    if player2.direction == 'left':
        screen.blit(pygame.transform.flip(pygame.transform.scale(player2.sprite,(20,45)),True,False),(camX+player2.X,camY+player2.Y))
    'END BLOCK'

    #switching weapons
    'START BLOCK'
    if keyboard.is_pressed('w') and player1.weaponswitch:
        try:
            player1.weapon = unlockedweapons[unlockedweapons.index(player1.weapon)+1]
        except:
            player1.weapon = unlockedweapons[0]

    if keyboard.is_pressed('up') and player2.weaponswitch:
        try:
            player2.weapon = unlockedweapons[unlockedweapons.index(player2.weapon)+1]
        except:
            player2.weapon = unlockedweapons[0]
    'END BLOCK'
    
    #sword
    'START BLOCK'
    #p1
    if player1.weapon == 'sword' or player1.weapon == 'morningstar':
        if player1.sword.sword > 0:
            player1.sword.sword = player1.sword.sword - 1
            
        if player1.sword.sword < 0:
            player1.sword.sword = player1.sword.sword + 1
            if player1.sword.sword == 0:
                player1.sword.sword = 30
            
        if keyboard.is_pressed('s'):
            if player1.sword.sword == 0:
                player1.sword.sword = -30
                player1.sword.length = 0
                player1.sword.state = 'out'

        if player1.sword.sword < 0: 
            if player1.sword.state == 'out':
                player1.sword.length = player1.sword.length + 1
                if player1.sword.length == 15:
                    player1.sword.state = 'in'

            if player1.sword.state == 'in':
                player1.sword.length = player1.sword.length - 1

            if player1.direction == 'left':
                screen.blit(player1.sword.sprite,(camX+player1.X-20-player1.sword.length,camY+player1.Y+10))
                player1.sword.rect.topleft = (player1.X-20-player1.sword.length,camY+player1.Y+15)
            if player1.direction == 'right':
                screen.blit(pygame.transform.flip(player1.sword.sprite,True,False),(camX+player1.X+10+player1.sword.length,camY+player1.Y+10))
                player1.sword.rect.topleft = (player1.X+10+player1.sword.length,camY+player1.Y+15)

    #p2
    if player2.weapon == 'sword' or player2.weapon == 'morningstar':
        if player2.sword.sword > 0:
            player2.sword.sword = player2.sword.sword - 1
            
        if player2.sword.sword < 0:
            player2.sword.sword = player2.sword.sword + 1
            if player2.sword.sword == 0:
                player2.sword.sword = 30
            
        if keyboard.is_pressed('down'):
            if player2.sword.sword == 0:
                player2.sword.sword = -30
                player2.sword.length = 0
                player2.sword.state = 'out'

        if player2.sword.sword < 0: 
            if player2.sword.state == 'out':
                player2.sword.length = player2.sword.length + 1
                if player2.sword.length == 15:
                    player2.sword.state = 'in'

            if player2.sword.state == 'in':
                player2.sword.length = player2.sword.length - 1

            if player2.direction == 'left':
                screen.blit(player2.sword.sprite,(camX+player2.X-20-player2.sword.length,camY+player2.Y+10))
                player2.sword.rect.topleft = (player2.X-20-player2.sword.length,camY+player2.Y+15)
            if player2.direction == 'right':
                screen.blit(pygame.transform.flip(player2.sword.sprite,True,False),(camX+player2.X+10+player2.sword.length,camY+player2.Y+10))
                player2.sword.rect.topleft = (player2.X+10+player2.sword.length,camY+player2.Y+15)
    'END BLOCK'

    #bow
    'START BLOCK'
    #p1
    if player1.weapon == 'bow':
        #cooldown
        if player1.bow.timer > 0:
            player1.bow.timer = player1.bow.timer - 1
            
        #pull
        if arrows > 0:
            if player1.bow.timer == 0:
                if keyboard.is_pressed('s'):
                    if player1.bow.pull < 50:
                        if player1.bow.pull < 10:
                            player1.bow.pull = 10
                        
                        player1.bow.pull = player1.bow.pull + 1

        #shoot
        if not keyboard.is_pressed('s') and not player1.bow.pull == 0:
            
            if player1.direction == 'left':
                arrowposition = (player1.rect.centerx+10,player1.rect.centery-10)
                arrowdirection = 'left'
                arrowmotion = (-5-(player1.bow.pull/5),0+random.uniform(-0.5,0.5))
            if player1.direction == 'right':
                arrowposition = (player1.rect.centerx+10,player1.rect.centery-10)
                arrowdirection = 'right'
                arrowmotion = (5+(player1.bow.pull/5),0+random.uniform(-0.5,0.5))

            #spawn new arrow
            projectiledata.append({'type':'arrow',
                                   'position':arrowposition,'motion':arrowmotion,'direction':arrowdirection,'gravity':True,
                                   'damage':0+player1.bow.pull/50})

            player1.bow.pull = 0
            player1.bow.timer = 40
            arrows = arrows - 1

        #draw bow
        if player1.bow.pull == 0:
            if player1.direction == 'left':
                screen.blit(pygame.transform.flip(bow,True,False),(camX+player1.rect.centerx-25,camY+player1.rect.centery-10))
            if player1.direction == 'right':
                screen.blit(bow,(camX+player1.rect.centerx+10,camY+player1.rect.centery-10))
        else: #draw the bow pulling
            if player1.direction == 'left':
                screen.blit(pygame.transform.flip(bowframe,True,False),(camX+player1.rect.centerx-25,camY+player1.rect.centery-10))
                #bowstring
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player1.rect.centerx-13,camY+player1.rect.centery-10), #start for the top half
                                 (camX+player1.rect.centerx-13+(player1.bow.pull/5),camY+player1.rect.centery),1) #end for the top half
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player1.rect.centerx-13+(player1.bow.pull/5),camY+player1.rect.centery), #start for the bottom half
                                 (camX+player1.rect.centerx-13,camY+player1.rect.centery+10),1) #end for the bottom half
                #arrow
                pygame.draw.line(screen,(90,20,0),
                                 (camX+player1.rect.centerx-13+(player1.bow.pull/5),camY+player1.rect.centery),
                                 (camX+player1.rect.centerx-40+(player1.bow.pull/5),camY+player1.rect.centery),1)
            if player1.direction == 'right':
                screen.blit(bowframe,(camX+player1.rect.centerx+10,camY+player1.rect.centery-10))
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player1.rect.centerx+16,camY+player1.rect.centery-10),
                                 (camX+player1.rect.centerx+16-(player1.bow.pull/5),camY+player1.rect.centery),1)
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player1.rect.centerx+16-(player1.bow.pull/5),camY+player1.rect.centery),
                                 (camX+player1.rect.centerx+16,camY+player1.rect.centery+10),1)
                pygame.draw.line(screen,(90,20,0),
                                 (camX+player1.rect.centerx+16-(player1.bow.pull/5),camY+player1.rect.centery),
                                 (camX+player1.rect.centerx+43-(player1.bow.pull/5),camY+player1.rect.centery),1)

    #p2
    if player2.weapon == 'bow':
        #cooldown
        if player2.bow.timer > 0:
            player2.bow.timer = player2.bow.timer - 1
            
        #pull
        if arrows > 0:
            if player2.bow.timer == 0:
                if keyboard.is_pressed('down'):
                    if player2.bow.pull < 50:
                        if player2.bow.pull < 10:
                            player2.bow.pull = 10
                        
                        player2.bow.pull = player2.bow.pull + 1

        #shoot
        if not keyboard.is_pressed('down') and not player2.bow.pull == 0:
            
            if player2.direction == 'left':
                arrowposition = (player2.rect.centerx+10,player2.rect.centery-10)
                arrowdirection = 'left'
                arrowmotion = (-5-(player2.bow.pull/5),0+random.uniform(-0.5,0.5))
            if player2.direction == 'right':
                arrowposition = (player2.rect.centerx+10,player2.rect.centery-10)
                arrowdirection = 'right'
                arrowmotion = (5+(player2.bow.pull/5),0+random.uniform(-0.5,0.5))

            #spawn new arrow
            projectiledata.append({'type':'arrow',
                                   'position':arrowposition,'motion':arrowmotion,'direction':arrowdirection,'gravity':True,
                                   'damage':0+player2.bow.pull/50})

            player2.bow.pull = 0
            player2.bow.timer = 40
            arrows = arrows - 1

        #draw bow
        if player2.bow.pull == 0:
            if player2.direction == 'left':
                screen.blit(pygame.transform.flip(bow,True,False),(camX+player2.rect.centerx-25,camY+player2.rect.centery-10))
            if player2.direction == 'right':
                screen.blit(bow,(camX+player2.rect.centerx+10,camY+player2.rect.centery-10))
        else: #draw the bow pulling
            if player2.direction == 'left':
                screen.blit(pygame.transform.flip(bowframe,True,False),(camX+player2.rect.centerx-25,camY+player2.rect.centery-10))
                #bowstring
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player2.rect.centerx-13,camY+player2.rect.centery-10), #start for the top half
                                 (camX+player2.rect.centerx-13+(player2.bow.pull/5),camY+player2.rect.centery),1) #end for the top half
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player2.rect.centerx-13+(player2.bow.pull/5),camY+player2.rect.centery), #start for the bottom half
                                 (camX+player2.rect.centerx-13,camY+player2.rect.centery+10),1) #end for the bottom half
                #arrow
                pygame.draw.line(screen,(90,20,0),
                                 (camX+player2.rect.centerx-13+(player2.bow.pull/5),camY+player2.rect.centery),
                                 (camX+player2.rect.centerx-40+(player2.bow.pull/5),camY+player2.rect.centery),1)
            if player2.direction == 'right':
                screen.blit(bowframe,(camX+player2.rect.centerx+10,camY+player2.rect.centery-10))
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player2.rect.centerx+16,camY+player2.rect.centery-10),
                                 (camX+player2.rect.centerx+16-(player2.bow.pull/5),camY+player2.rect.centery),1)
                pygame.draw.line(screen,(255,255,255),
                                 (camX+player2.rect.centerx+16-(player2.bow.pull/5),camY+player2.rect.centery),
                                 (camX+player2.rect.centerx+16,camY+player2.rect.centery+10),1)
                pygame.draw.line(screen,(90,20,0),
                                 (camX+player2.rect.centerx+16-(player2.bow.pull/5),camY+player2.rect.centery),
                                 (camX+player2.rect.centerx+43-(player2.bow.pull/5),camY+player2.rect.centery),1)
    'END BLOCK'

    #boomerang
    'START BLOCK'
    #p1
    if player1.weapon == 'boomerang':
        #draw holding the boomerang
        if not player1.boomerang.thrown:
            if player1.direction == 'left':
                screen.blit(pygame.transform.rotate(boomerang,player1.boomerang.rotation),
                            (camX+player1.rect.centerx-25,camY+player1.rect.centery-10))
            if player1.direction == 'right':
                screen.blit(pygame.transform.flip(pygame.transform.rotate(boomerang,player1.boomerang.rotation),True,False),
                            (camX+player1.rect.centerx+10,camY+player1.rect.centery-10))
        #cooldown
        if player1.boomerang.cooldown > 0:
            player1.boomerang.cooldown = player1.boomerang.cooldown - 1
            
        #throw
        if keyboard.is_pressed('s'):
            if not player1.boomerang.thrown:
                if player1.boomerang.cooldown == 0:
                    player1.boomerang.position = (player1.rect.centerx,player1.rect.centery-15)
                    player1.boomerang.thrown = True
                    player1.boomerang.speed = 20
                    player1.boomerang.direction = player1.direction
                    player1.boomerang.rotation = player1.boomerang.rotation % 360

        #move
        if player1.boomerang.thrown:
            if player1.boomerang.direction == 'left':
                player1.boomerang.position = (player1.boomerang.position[0]-player1.boomerang.speed,player1.boomerang.position[1])
            if player1.boomerang.direction == 'right':
                player1.boomerang.position = (player1.boomerang.position[0]+player1.boomerang.speed,player1.boomerang.position[1])

            player1.boomerang.rotation = player1.boomerang.rotation + 10
            player1.boomerang.speed = player1.boomerang.speed - 1
            player1.boomerang.rect.topleft = player1.boomerang.position

            #draw
            if player1.boomerang.direction == 'left':
                screen.blit(pygame.transform.rotate(boomerang,player1.boomerang.rotation),(camX+player1.boomerang.position[0],camY+player1.boomerang.position[1]))
            if player1.boomerang.direction == 'right':
                screen.blit(pygame.transform.flip(pygame.transform.rotate(boomerang,player1.boomerang.rotation),True,False),(camX+player1.boomerang.position[0],camY+player1.boomerang.position[1]))
            player1.boomerang.rect.topleft = player1.boomerang.position

            #despawn if returned to player
            if player1.boomerang.rect.colliderect(player1.rect):
                if player1.boomerang.speed < 0:
                    player1.boomerang.thrown = False
                    player1.boomerang.cooldown = 20

    #p2
    if player2.weapon == 'boomerang':
        #draw holding the boomerang
        if not player2.boomerang.thrown:
            if player2.direction == 'left':
                screen.blit(pygame.transform.rotate(boomerang,player2.boomerang.rotation),
                            (camX+player2.rect.centerx-25,camY+player2.rect.centery-10))
            if player2.direction == 'right':
                screen.blit(pygame.transform.flip(pygame.transform.rotate(boomerang,player2.boomerang.rotation),True,False),
                            (camX+player2.rect.centerx+10,camY+player2.rect.centery-10))
        #cooldown
        if player2.boomerang.cooldown > 0:
            player2.boomerang.cooldown = player2.boomerang.cooldown - 1
            
        #throw
        if keyboard.is_pressed('down'):
            if not player2.boomerang.thrown:
                if player2.boomerang.cooldown == 0:
                    player2.boomerang.position = (player2.rect.centerx,player2.rect.centery-15)
                    player2.boomerang.thrown = True
                    player2.boomerang.speed = 20
                    player2.boomerang.direction = player2.direction
                    player2.boomerang.rotation = player2.boomerang.rotation % 360

        #move
        if player2.boomerang.thrown:
            if player2.boomerang.direction == 'left':
                player2.boomerang.position = (player2.boomerang.position[0]-player2.boomerang.speed,player2.boomerang.position[1])
            if player2.boomerang.direction == 'right':
                player2.boomerang.position = (player2.boomerang.position[0]+player2.boomerang.speed,player2.boomerang.position[1])

            player2.boomerang.rotation = player2.boomerang.rotation + 10
            player2.boomerang.speed = player2.boomerang.speed - 1
            player2.boomerang.rect.topleft = player2.boomerang.position

            #draw
            if player2.boomerang.direction == 'left':
                screen.blit(pygame.transform.rotate(boomerang,player2.boomerang.rotation),(camX+player2.boomerang.position[0],camY+player2.boomerang.position[1]))
            if player2.boomerang.direction == 'right':
                screen.blit(pygame.transform.flip(pygame.transform.rotate(boomerang,player2.boomerang.rotation),True,False),(camX+player2.boomerang.position[0],camY+player2.boomerang.position[1]))
            player1.boomerang.rect.topleft = player2.boomerang.position

            #despawn if returned to player
            if player2.boomerang.rect.colliderect(player2.rect):
                if player2.boomerang.speed < 0:
                    player2.boomerang.thrown = False
                    player2.boomerang.cooldown = 20
    'END BLOCK'
                                 
    #projectiles
    'START BLOCK'
    for projectile in projectiledata:
        #move
        projectile['position'] = (projectile['position'][0]+projectile['motion'][0],projectile['position'][1]+projectile['motion'][1])
        if projectile['gravity']:
            projectile['motion'] = (projectile['motion'][0],projectile['motion'][1]+0.1)
        #delete if touching the ground
        if projectile['position'][1] > 500:
            projectiledata.remove(projectile)
        #render
        if projectile['direction'] == 'left':
            screen.blit(pygame.transform.flip(arrow,True,False),(camX+projectile['position'][0],camY+projectile['position'][1]))
        if projectile['direction'] == 'right':
            screen.blit(arrow,(camX+projectile['position'][0],camY+projectile['position'][1]))
    'END BLOCK'
    
    #enemy spawning
    'START BLOCK'
    enemytimer = enemytimer - 1

    #spawn enemies
    if enemytimer < 1:

        #generate all the enemy data
        if random.randint(0,1) == 1:
            newenemyX = -100
        else:
            newenemyX = 1300

        newenemyhealth = random.randint(2,4) * difficulty
        newenemyspeed = random.uniform(0.8,1.5) * difficulty
        newenemydamage = random.uniform(2,5) * difficulty

        #spawn new enemy
        enemies.append({'type':'normal',
                        'X':newenemyX-camX,'Y':460+camY,'direction':'left','knockback':0,
                        'target':'none','targettimer':0,'speed':newenemyspeed,
                        'health':newenemyhealth,'hurttimer':0,
                        'attacktimer':0,'damage':newenemydamage})
            
        enemytimer = random.randint(400,600) / difficulty

    #clear dead enemies
    for enemy in enemies:
        if enemy['health'] < 1:
            enemies.remove(enemy)
    'END BLOCK'

    #enemy AI
    'START BLOCK'
    for enemy in enemies:

        if enemy['type'] == 'normal':
            enemyrect = zombie1.get_rect()
            enemyrect.topleft = (enemy['X'],enemy['Y'])

            #whether or not the zombie can take damage
            if enemy['hurttimer'] > 0:
                enemy['hurttimer'] = enemy['hurttimer'] - 1

            #targeting
            if enemy['targettimer'] > 0:
                enemy['targettimer'] = enemy['targettimer'] - 1

            if enemy['targettimer'] == 0:
                if math.dist(enemyrect.center,player1.rect.center) < math.dist(enemyrect.center,player2.rect.center):
                    if player1.currenthouse == 'none':
                        enemy['target'] = '1'
                        enemy['targettimer'] = 120
                    else:
                        enemy['target'] = '2'
                        enemy['targettimer'] = 120
                if math.dist(enemyrect.center,player2.rect.center) < math.dist(enemyrect.center,player1.rect.center):
                    if player2.currenthouse == 'none':
                        enemy['target'] = '2'
                        enemy['targettimer'] = 120
                    else:
                        enemy['target'] = 1
                        enemy['targettimer'] = 120

            #chase            
            if enemy['target'] == '1' and not abs(enemyrect.centerx-player1.rect.centerx) < 1:
                if enemyrect.centerx > player1.rect.centerx:
                    enemy['X'] = enemy['X'] - enemy['speed']
                    enemy['direction'] = 'left'
                if enemyrect.centerx < player1.rect.centerx:
                    enemy['X'] = enemy['X'] + enemy['speed']
                    enemy['direction'] = 'right'
        
            if enemy['target'] == '2' and not abs(enemyrect.centerx-player2.rect.centerx) < 15:
                if enemyrect.centerx > player2.rect.centerx:
                    enemy['X'] = enemy['X'] - enemy['speed']
                    enemy['direction'] = 'left'
                if enemyrect.centerx < player2.rect.centerx:
                    enemy['X'] = enemy['X'] + enemy['speed']
                    enemy['direction'] = 'right'

            #when hit by sword
            if (enemyrect.colliderect(player1.sword.rect) and player1.sword.sword < 0 and player1.currenthouse == 'none'):
                if enemy['hurttimer'] == 0:
                    if unlockedweapons[0] == 'morningstar':
                        enemy['health'] = enemy['health'] - 3
                    else:
                        enemy['health'] = enemy['health'] - 1
                    if player1.direction == 'left':
                        enemy['knockback'] = -7
                    if player1.direction == 'right':
                        enemy['knockback'] = 7
                    enemy['hurttimer'] = 40
            if (enemyrect.colliderect(player2.sword.rect) and player2.sword.sword < 0 and player2.currenthouse == 'none'):
                if enemy['hurttimer'] == 0:
                    if unlockedweapons[0] == 'morningstar':
                        enemy['health'] = enemy['health'] - 3
                    else:
                        enemy['health'] = enemy['health'] - 1
                    if player2.direction == 'left':
                        enemy['knockback'] = -7
                    if player2.direction == 'right':
                        enemy['knockback'] = 7
                    enemy['hurttimer'] = 40

            #when hit by arrow
            for projectile in projectiledata:
                if projectile['type'] == 'arrow':
                    if enemyrect.collidepoint(projectile['position']):
                        enemy['health'] = enemy['health'] - projectile['damage']
                        if projectile['direction'] == 'left':
                            enemy['knockback'] = -(int(abs(projectile['motion'][0]))-5)
                        if projectile['direction'] == 'right':
                            enemy['knockback'] = int(abs(projectile['motion'][0]))-5
                        projectiledata.remove(projectile)

            #when hit by boomerang
            if enemyrect.colliderect(player1.boomerang.rect) and player1.boomerang.thrown:
                enemy['health'] = enemy['health'] - 0.3
                if player1.boomerang.direction == 'left':
                    enemy['knockback'] = -4
                if player1.boomerang.direction == 'right':
                    enemy['knockback'] = 4
                enemy['hurttimer'] = 40
                player1.boomerang.speed = 0
                
            if enemyrect.colliderect(player2.boomerang.rect) and player2.boomerang.thrown:
                enemy['health'] = enemy['health'] - 0.3
                if player2.boomerang.direction == 'left':
                    enemy['knockback'] = -4
                if player2.boomerang.direction == 'right':
                    enemy['knockback'] = 4
                enemy['hurttimer'] = 40
                player2.boomerang.speed = 0


            #takes knockback
            if enemy['knockback'] != 0:
                enemy['X'] = enemy['X'] + enemy['knockback']
            if enemy['knockback'] > 0:
                enemy['knockback'] = enemy['knockback'] - 1
            if enemy['knockback'] < 0:
                enemy['knockback'] = enemy['knockback'] + 1

            #attack
            if enemy['target'] == '1':
                if abs(enemyrect.centerx-player1.rect.centerx) < 30 and player1.currenthouse == 'none':
                    if enemy['attacktimer'] == 0:
                        enemy['attacktimer'] = 40
                    else:
                        enemy['attacktimer'] = enemy['attacktimer'] - 1
                        if enemy['attacktimer'] == 0:
                            health = health - enemy['damage']

            if enemy['target'] == '2':
                if abs(enemyrect.centerx-player2.rect.centerx) < 30 and player2.currenthouse == 'none':
                    if enemy['attacktimer'] == 0:
                        enemy['attacktimer'] = 40
                    else:
                        enemy['attacktimer'] = enemy['attacktimer'] - 1
                        if enemy['attacktimer'] == 0:
                            health = health - enemy['damage']
                              
            #draws the sprite
            if enemy['direction'] == 'left':
                screen.blit(pygame.transform.flip(zombie1,True,False),(camX+enemy['X'],camY+enemy['Y']))
            if enemy['direction'] == 'right':
                screen.blit(zombie1,(camX+enemy['X'],camY+enemy['Y']))
    'END BLOCK'

    #makes it so the player doesnt switch super fast if you hold interact down
    #this goes at the end of the loop for reasons
    'START BLOCK'
    if not keyboard.is_pressed('w'):
        player1.weaponswitch = True
    else:
        player1.weaponswitch = False
        
    if not keyboard.is_pressed('up'):
        player2.weaponswitch = True
    else:
        player2.weaponswitch = False
    'END BLOCK'

    #displays
    'START BLOCK'
    #health counter
    #makes it so the health counter will never read 0
    if round(health) == 0:
        healthrounded = '1'
    else:
        healthrounded = str(round(health))
    healthdisplay = font.render(healthrounded,True,(0,0,0))
    screen.blit(heart,(30,30))
    screen.blit(healthdisplay,(60,30))

    #arrows counter
    if 'bow' in unlockedweapons:
        arrowdisplay = font.render(str(arrows),True,(0,0,0))
        screen.blit(arrowicon,(30,60))
        screen.blit(arrowdisplay,(60,65))
    'END BLOCK'
    
    #necessary stuff
    'START BLOCK'
    pygame.display.update()
    clock.tick(60)
    'END BLOCK'

#quit
pygame.quit()
