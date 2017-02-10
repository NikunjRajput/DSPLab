import pygame

import time

import random
from os import system
from texttosound_timescale import time_scale
from texttosound_timescale import time_scale1


#from myfunctions import pitch
pygame.init()







#crash_sound = pygame.mixer.Sound()

#from pygame.locals import *

#screen = pygame.display.set_mode((1024, 768))

#screen = pygame.display.set_mode((1024, 768), FULLSCREEN)

                                 
List1 = []
List2 = []
List3 = ["aa","bb","cc","dd","ee","ff","gg","hh","ii","jj"]
output_wavefile = ""
output_wavefile1 = ""

                                 

display_width = 750

display_height = 750
output_wavefile = 'demo.wav'

 

black = (0,0,0)

white = (255,255,255)

cyan = (224,255,255)

yellow = (255,255,0)



red = (200,0,0)

green = (0,200,0)



bright_red = (255,0,0)

bright_green = (0,255,0)

 

block_color = (255,255,0)

 

car_width = 200

 

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('DSP Final Project Game')

clock = pygame.time.Clock()

 

carImg = pygame.image.load('pygameimage.jpg')

gameIcon = pygame.image.load('pygameimage.jpg')



pygame.display.set_icon(gameIcon)



pause = False

#crash = True

 

def things_hit(count):

    font = pygame.font.SysFont("comicsansms", 25)

    text = font.render("hit: "+str(count), True, cyan)

    gameDisplay.blit(text,(0,0))

 

def things(thingx, thingy, thingw, thingh, color):

    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

 

def car(x,y):

    gameDisplay.blit(carImg,(x,y))

 

def text_objects(text, font):

    textSurface = font.render(text, True, cyan)

    return textSurface, textSurface.get_rect()

 

 

def crash():

    #pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.load(output_wavefile1)

    pygame.mixer.music.play(-1)

    pygame.mixer.music.stop()

    largeText = pygame.font.SysFont("comicsansms",80)

    TextSurf, TextRect = text_objects("You Crashed", largeText)

    TextRect.center = ((display_width/2),(display_height/2))

    gameDisplay.blit(TextSurf, TextRect)

    



    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

                

        

        


        button("Play Again",150,450,100,50,green,bright_green,game_loop)

        button("Quit",550,450,100,50,red,bright_red,quitgame)



        pygame.display.update()

        clock.tick(15) 



def button(msg,x,y,w,h,ic,ac,action=None):

    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()



    if x+w > mouse[0] > x and y+h > mouse[1] > y:

        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            #print action
            #print 'Raj'

            action()         

    else:

        #print "Nik"

        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)

    textSurf, textRect = text_objects(msg, smallText)

    textRect.center = ( (x+(w/2)), (y+(h/2)) )

    gameDisplay.blit(textSurf, textRect)

    



def quitgame():

    pygame.quit()

    quit()



def unpause():

    global pause

    pygame.mixer.music.unpause()

    pause = False

    



def paused():

    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicsansms",80)

    TextSurf, TextRect = text_objects("Paused", largeText)

    TextRect.center = ((display_width/2),(display_height/2))

    gameDisplay.blit(TextSurf, TextRect)

    



    while pause:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()





        button("Continue",130,500,100,50,green,bright_green,unpause)

        button("Quit",530,500,100,50,red,bright_red,quitgame)



        pygame.display.update()

        clock.tick(15)   





def game_intro():

    global pause
   
    #pygame.mixer.music.load('intro.wav')

    #pygame.mixer.music.play(-1)



    intro = True




    while intro:

        #while intro:

        for event in pygame.event.get():

            #print(event)

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

        gameDisplay.fill(black)

        largeText = pygame.font.SysFont("arial",40)

        TextSurf, TextRect = text_objects("Final Project Demo", largeText)
        TextRect.center = ((350),(100))
        gameDisplay.blit(TextSurf, TextRect)

        global pause
        button("Level-1",200,200,80,50,black,black,slow1)
        button("Level-2",200,300,80,50,black,black,slow1)
        button("Level-3",200,400,80,50,black,black,slow1)
        button("Slow",400,200,80,50,green,bright_green,slow1)
        button("Medium",500,200,80,50,green,bright_green,medium1)
        button("Fast",600,200,80,50,green,bright_green,fast1)
        button("Slow",400,300,80,50,green,bright_green,slow2)
        button("Medium",500,300,80,50,green,bright_green,medium2)
        button("Fast",600,300,80,50,green,bright_green,fast2)
        button("Slow",400,400,80,50,green,bright_green,slow3)
        button("Medium",500,400,80,50,green,bright_green,medium3)
        button("Fast",600,400,80,50,green,bright_green,fast3)
        button("Play",130,500,80,50,green,bright_green,game_loop)
        button("Quit",530,500,100,50,red,bright_red,quitgame)



        pygame.display.update()

        clock.tick(15)
        #intro = False


        

def slow1():
    #print "LLL"
    
    global pause
    


    if (List3[0]=="aa") :
        system('say Playing Level 1 Slow Music!')
        print List1.append('demo1')
        print List2.append('1')
        print List1
        print List2
        List3[0] = ["a"]
        pygame.display.update() 

def slow2():
    #print "LLL"
    
    global pause


    if (List3[1]=="bb") :
        system('say Playing Level 2 Slow Music!')
        print List1.append('Hello1')
        print List2.append('1')
        print List1
        print List2
        List3[1] = ["b"]
        pygame.display.update()                

def slow3():
    #print "LLL"
    
    global pause


    if (List3[2]=="cc") :
        system('say Playing Level 3 Slow Music!')
        print List1.append('Hello2')
        print List2.append('1')
        print List1
        print List2
        List3[2] = ["d"]
        pygame.display.update() 

def medium1():
    #print "LLL"
    
    global pause


    if (List3[3]=="dd") :
        system('say Playing Level 1 Medium Music!')
        print List1.append('demo1')
        print List2.append('2')
        print List1
        print List2
        List3[3] = ["d"]
        pygame.display.update() 
def medium2():
    # print "LLL"
    
    global pause


    if (List3[4]=="ee") :
        system('say Playing Level 2 Medium Music!')
        print List1.append('Hello1')
        print List2.append('2')
        print List1
        print List2
        List3[4] = ["e"]
        pygame.display.update() 
def medium3():
    #print "LLL"
    
    global pause


    if (List3[5]=="ff") :
        system('say Playing Level 3 Medium Music!')
        print List1.append('Hello2')
        print List2.append('3')
        print List1
        print List2
        List3[5] = ["f"]
        pygame.display.update()  
def fast1():
    #print "LLL"
    
    global pause


    if (List3[6]=="gg") :
        system('say Playing Level 1 Fast Music!')
        print List1.append('demo1')
        print List2.append('3')
        print List1
        print List2
        List3[6] = ["g"]
        pygame.display.update() 
def fast2():
    #print "LLL"
    
    global pause


    if (List3[7]=="hh") :
        system('say Playing Level 2 Fast Music!')
        print List1.append('Hello1')
        print List2.append('3')
        print List1
        print List2
        List3[7] = ["h"]
        pygame.display.update() 
def fast3():
    # print "LLL"
    
    global pause


    if (List3[8]=="ii") :
        system('say Playing Level 3 Fast Music!')
        print List1.append('Hello2')
        print List2.append('3')
        print List1
        print List2
        List3[8] = ["i"]
        pygame.display.update()                                               
    

    



def game_loop():
    #print "LLL"

    global pause

    if (List3[9]=="jj") :
        #output_wavefile = 'aa.wav'
        print 'lalala'
        output_wavefile1 = time_scale1(List1[0],List2[0])
        output_wavefile2 = time_scale1(List1[1],List2[1])
        output_wavefile3 = time_scale1(List1[2],List2[2])
        crash_sound = pygame.mixer.Sound(output_wavefile3)
        #pygame.mixer.Sound.play(crash_sound)
        print output_wavefile1
        print output_wavefile2
        print output_wavefile3

        pygame.display.update()
        List3[9] = ["j"]
        pygame.display.update()
    
    print 'song'
    print output_wavefile
    pygame.mixer.music.load(output_wavefile1)

    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)

    y = (display_height * 0.8)

 

    x_change = 0
    s = 1
    tscale = 0

    

    thing_startx = random.randrange(0, display_width)

    thing_starty = -500

    thing_speed = 5

    thing_width = 100

    thing_height = 100
    

 

    thingCount = 1
    #    t=60
 

    hit = 0
    

 

    gameExit = False

 

    while not gameExit:

 

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

 

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    x_change = -5 - s

                if event.key == pygame.K_RIGHT:

                    x_change = 5 + s

                if event.key == pygame.K_p:

                    pause = True

                    paused()

                    

 

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                    x_change = 0

 

        x += x_change

#print x

        gameDisplay.fill(black)

 

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)

 

 

        

        thing_starty += thing_speed

        car(x,y)

        things_hit(hit)

 

        if x > display_width - car_width or x < 0:

            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            hit += 1
            
            thing_width += (hit * 1.2)
            
            if hit%2 == 0 :
                hit = 0
                s = s + 1
                thing_speed += 1
            
            if hit == 0 :

            	
                system('say Second Hit!')
                system('say Next Level!')

                

            if hit == 1 :
                system('say First Hit!')
#                print ('Nik')
#                tscale = tscale + .0009
#                                
#                s = s+4
#                print tscale
#                time_scale(tscale,output_wavefile)
#                print output_wavefile
#
#                t=t+.7

                                                    
        if y < thing_starty+thing_height:
            #print('y crossover')
            if thing_startx <= x or thing_startx > x + car_width:
                #print('x crossover')
                crash()
 #if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                #              crash()
        pygame.display.update()

        clock.tick(60)

#output_wavefile = 'demo.wav'
#tscale = 5
#filecount = 0
#if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
#              crash()
game_intro()

game_loop()

pygame.quit()

quit()

