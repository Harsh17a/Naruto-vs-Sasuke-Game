#Import modules
import pygame
import random
import button

pygame.init()

#Setup screen
width=700
height=500
screen=pygame.display.set_mode((width,height))
surface=pygame.Surface((width,height),pygame.SRCALPHA)
pygame.display.set_caption("Naruto vs Sasuke")
clock=pygame.time.Clock()
running=True
pause=False
restart=False
home_screen=False

#Load Images
walkRight=[pygame.image.load("Assets//NR2.png"),pygame.image.load("Assets//NR3.png"),pygame.image.load("Assets//NR1.png")]
walkLeft=[pygame.image.load("Assets//NL2.png"),pygame.image.load("Assets//NL3.png"),pygame.image.load("Assets//NL1.png")]
background=pygame.image.load("Assets//bg.png")
naruto_stand=pygame.image.load("Assets//Nstanding.png")
naruto_head=pygame.image.load("Assets//Nh.png")
sasuke_head=pygame.image.load("Assets//Sh.png")
shuriken_img=pygame.image.load("Assets//shur.png")
gameover_img=pygame.image.load("Assets//gameover.jpg")

#Load Sound
hit_sound=pygame.mixer.Sound("Assets//hit.wav")
shur_sound=pygame.mixer.Sound("Assets//shuriken.wav") 
bgm=pygame.mixer.music.load("Assets//theme.mp3")

#load buttons images
start_img=pygame.image.load("Assets//start_button.png")
help_img=pygame.image.load("Assets//help_button.png")
pause_img=pygame.image.load("Assets//pause_button.png")
options_img=pygame.image.load("Assets//options 3.jpg")
resume_img=pygame.image.load("Assets//resume.jpg")
replay_img=pygame.image.load("Assets//replay.jpg")
exit_img=pygame.image.load("Assets//exit.jpg")
home_img=pygame.image.load("Assets//home_button.png")
back_img=pygame.image.load("Assets//back_button.png")

#Edit images
options_image=pygame.transform.scale(options_img,(int(options_img.get_width() * 0.7), int(options_img.get_height() * 0.7)))
resume_image= pygame.transform.scale(resume_img, (int(resume_img.get_width() * 0.7), int(resume_img.get_height() * 0.7)))
restart_image= pygame.transform.scale(replay_img, (int(replay_img.get_width() * 0.7), int(replay_img.get_height() * 0.7)))
exit_image= pygame.transform.scale(exit_img, (int(exit_img.get_width() * 0.7), int(exit_img.get_height() * 0.7)))
home_image= pygame.transform.scale(home_img, (int(home_img.get_width() * 0.2), int(home_img.get_height() * 0.2)))
gameover_image= pygame.transform.scale(gameover_img, (int(gameover_img.get_width() * 0.2), int(gameover_img.get_height() * 0.2)))

#make Buttons
start_button=button.Button(270,150,start_img,0.3)
help_button=button.Button(276,240,help_img,0.5)
pause_button=button.Button(320,30,pause_img,0.2)
resume_button=button.Button(272,171,resume_img,0.7)
restart_button=button.Button(270,240,replay_img,0.7)
exit_button=button.Button(270,310,exit_img,0.7)
home_button=button.Button(310,370,home_img,0.2)
back_button=button.Button(2,2,back_img,0.5)

restart_button_1=button.Button(220,240,replay_img,0.5)
exit_button_1=button.Button(370,240,exit_img,0.5)


#Player Class
class Player:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.speed=10
        self.is_jump=False
        self.jumpheight=10
        self.left=False
        self.right=False
        self.walkcount=0
        self.standing=True
        self.hitbox=(self.x +10 ,self.y +5 ,80,80)
        self.health=200
        self.damage=0

    #Draw Naruto 
    def draw_naruto(self,screen):
        if self.health >0:
            if self.walkcount +1 > 6:
                self.walkcount=0
        
            if not (self.standing):
                if self.left:
                    screen.blit(walkLeft[self.walkcount//2],(self.x,self.y))
                    self.walkcount+=1
            
                elif self.right:
                    screen.blit(walkRight[self.walkcount//2],(self.x,self.y))
                    self.walkcount+=1
            else:
                if self.right:
                    screen.blit(pygame.image.load("Assets//NR1.png"),(self.x,self.y))
                else:
                    screen.blit(pygame.image.load("Assets//NL1.png"),(self.x,self.y))
        
            self.hitbox=(self.x +10 ,self.y +5 ,80,80) #Make Hitbox
            Nbar2=pygame.draw.rect(screen,(255,0,0),(410,40,202,25))
            Nbar=pygame.draw.rect(screen,(0,255,0),(412+self.damage,45,200-self.damage,15))
            
        #If Naruto loss
        else:
            self.speed=0
            screen.blit(pygame.image.load("Assets//Nd.png"),(self.x,400))
            
            game_over("Sasuke Wins","blue")

    #Naruto Hitbox
    def hit(self):
        if self.health >0:
            self.health-=10
            self.damage+=10

#Sasuke Class
class Enemy:
    #Load Images
    walkRight_S=[pygame.image.load("Assets//SR2.png"),pygame.image.load("Assets//SR3.png"),pygame.image.load("Assets//SR1.png")]
    walkLeft_S=[pygame.image.load("Assets//SL2.png"),pygame.image.load("Assets//SL3.png"),pygame.image.load("Assets//SL1.png")]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.left=False
        self.right=False
        self.speed=8
        self.walkcount=0
        self.is_jump=False
        self.jumpheight=10
        self.hitbox=(self.x +10 ,self.y +5 ,80,80)
        self.health=200
        self.s_hit=False
    
    #Move Sasuke
    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x+=self.speed
            else:
                self.speed = self.speed * -1
                self.walkcount=0
        
        else:
            if self.x - self.speed > self.path[0]:
                self.x+=self.speed
            else:
                self.speed = self.speed * -1
                self.walkcount=0
    
    #Jump Sasuke
    def jump(self):
        if self.is_jump == False:
            if random.randint(1,20)==1 or self.s_hit==True:
                self.is_jump=True
                self.walkcount=0
        
        #Down Sasuke
        else:
            if self.jumpheight >= -10:
                neg=1
                if self.jumpheight <0:
                    neg=-1
                self.y -=(self.jumpheight ** 2)* 0.5 * neg
                self.jumpheight -=1
            else:
                self.is_jump=False
                self.s_hit=False
                self.jumpheight=10
    
    #Draw Sasuke
    def draw_enemy(self,screen):
        self.move()
        if self.health > 0:
            if self.walkcount +1 > 6:
                self.walkcount=0
            
            if self.speed > 0:
                screen.blit(self.walkRight_S[self.walkcount//2],(self.x,self.y))
                self.left=False
                self.right=True
                self.walkcount+=1
            else:
                screen.blit(self.walkLeft_S[self.walkcount//2],(self.x,self.y))
                self.left=True
                self.right=False
                self.walkcount+=1
        
            self.hitbox=(self.x +10 ,self.y +5 ,80,80) #Draw hitbox 
            Sbar2=pygame.draw.rect(screen,(255,0,0),(80,40,202,25))
            Sbar=pygame.draw.rect(screen,(0,255,0),(80,45,self.health,15))
        
        #If Sasuke Loss
        else:
            self.speed=0
            screen.blit(pygame.image.load("Assets//Sd.png"),(self.x,400))
            game_over("Naruto Wins","orange")
    
    #Sasuke Hitbox
    def hit(self):
        if self.health >0:
            self.health-=10

#Weapons Class
class Weapons:
    def __init__(self,x,y,width,height,facing):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.facing=facing
        self.vel=15 * facing
        self.s_vel=15 * facing
        self.hitbox=(self.x,self.y,40,40)
    
    #Draw Naruto shuriken
    def naruto_shuriken(self,screen):
        shuriken_image=pygame.image.load("Assets//shur.png")
        screen.blit(shuriken_image,(self.x,self.y))
        self.hitbox=(self.x,self.y,40,40)
    
    #Draw Sasuke shuriken
    def sasuke_shuriken(self,screen):
        shuriken_image=pygame.image.load("Assets//shur2.png") 
        screen.blit(shuriken_image,(self.x,self.y))
        self.hitbox=(self.x,self.y,40,40)



#Naruto Weapon
def naruto_weapon(keys):
    global N_throw_speed
    
    if N_throw_speed>0:
        N_throw_speed+=1
    
    if N_throw_speed>3:
        N_throw_speed=0
    
    if keys[pygame.K_SPACE] and N_throw_speed==0:
        if naruto.left==True:
            facing=-1
        else:
            facing=1
    
        if len(naruto_shurikens)<3:
            naruto_shurikens.append(Weapons(naruto.x+30,naruto.y+30,40,40,facing))
    
        N_throw_speed=1
        shur_sound.play()

#Sasuke Weapon
def sasuke_weapon():
    global S_throw_speed
    
    if S_throw_speed>0:
        S_throw_speed+=1
    
    if S_throw_speed>3:
        S_throw_speed=0
    
    if S_throw_speed==0:
        if sasuke.left==True:
            facing=-1
        else:
            facing=1
    
        if len(sasuke_shurikens)<5:
            sasuke_shurikens.append(Weapons(sasuke.x+30,sasuke.y+30,40,40,facing))
    
        S_throw_speed=1
        shur_sound.play()

#Display Images on screen
def display_image():
    global pause
    
    screen.blit(background,(0,0))
    naruto.draw_naruto(screen)
    sasuke.draw_enemy(screen)
    screen.blit(naruto_head,(600,10))#10,10
    screen.blit(sasuke_head,(10,10))#600,10
    
    for shuriken in naruto_shurikens:
        if naruto.health >0 :
            if sasuke.health > 0:
                if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > sasuke.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < sasuke.hitbox[1] +sasuke.hitbox[3]:
                    if shuriken.hitbox[0] + shuriken.hitbox[2] > sasuke.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < sasuke.hitbox[0] +sasuke.hitbox[2]:
                        sasuke.hit()
                        sasuke.s_hit=True
                        hit_sound.play()
                        naruto_shurikens.pop(naruto_shurikens.index(shuriken))
            
            shuriken.naruto_shuriken(screen)
    
    for shuriken in sasuke_shurikens:
        if sasuke.health >0:
            if naruto.health > 0:
                if shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) > naruto.hitbox[1] and shuriken.hitbox[1] + round(shuriken.hitbox[3]/2) < naruto.hitbox[1] +naruto.hitbox[3]:
                    if shuriken.hitbox[0] + shuriken.hitbox[2] > naruto.hitbox[0] and shuriken.hitbox[0] + shuriken.hitbox[2] < naruto.hitbox[0] +naruto.hitbox[2]:
                        naruto.hit()
                        hit_sound.play()
                        sasuke_shurikens.pop(sasuke_shurikens.index(shuriken))
            
            shuriken.sasuke_shuriken(screen)
    
    if pause_button.draw(screen):
        pause=True
        pause_screen()
    
    pygame.display.update()

#Movements of Naruto
def move_naruto(keys):
    if sasuke.health>0:
        naruto_weapon(keys) #Naruto Weapon
    
    if not pause and naruto.health>0:
        if random.randint(1,4) == 1:
            sasuke_weapon() #Sasuke Weapon
    
    #Turn Naruto Left
    if keys[pygame.K_LEFT] and naruto.x >3:  
        naruto.x-=naruto.speed
        naruto.left=True
        naruto.right=False
        naruto.standing=False
    
    #Turn Naruto Right
    elif keys[pygame.K_RIGHT] and naruto.x < 700 - naruto.width:
        naruto.x+=naruto.speed
        naruto.left=False
        naruto.right=True
        naruto.standing=False
    
    #Standing position
    else:
        naruto.standing=True
        naruto.walkcount=0
    
    #Jump Naruto
    if naruto.health>0:
        if naruto.is_jump == False:
            if keys[pygame.K_UP]:
                naruto.is_jump=True
                naruto.walkcount=0

        #Down Naruto
        else:
            if naruto.jumpheight >= -10:
                neg=1
                if naruto.jumpheight <0:
                    neg=-1
                naruto.y -=(naruto.jumpheight ** 2)* 0.5 * neg
                naruto.jumpheight -=1
            else:
                naruto.is_jump=False
                naruto.jumpheight=10
    
    if sasuke.health>0:
        sasuke.jump()
    
    display_image()



#Create objects
naruto=Player(650,400,100,100)
sasuke=Enemy(30,400,100,100,600)
font=pygame.font.SysFont("comicsans",30,True)
naruto_shurikens=[]
N_throw_speed=0
sasuke_shurikens=[]
S_throw_speed=0



#Main loop
def mainloop():
    global running,pause,restart,home_screen
    running=True
    pygame.mixer.music.play() #Play Background Music
    while running:
        restart=False
        home_screen=False
        clock.tick(25)
        
        if pause:
            if resume_button.draw(screen):
                pause=False
            
            if restart_button.draw(screen):
                restart=True
                pause=False
                running=False
            
            if exit_button.draw(screen):
                running=False
            
            if home_button.draw(screen):
                running=False
                home_screen=True
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running=False
        
        for shuriken in naruto_shurikens:
            if shuriken.x > 0 and shuriken.x < 699:
                shuriken.x +=shuriken.vel
            else:
                naruto_shurikens.pop(naruto_shurikens.index(shuriken))
                
        for shuriken in sasuke_shurikens:
            if shuriken.x > 0 and shuriken.x < 699:
                shuriken.x +=shuriken.s_vel
            else:
                sasuke_shurikens.pop(sasuke_shurikens.index(shuriken))
                
        
        keys=pygame.key.get_pressed()
        
        if not pause: 
            move_naruto(keys)
    
    else:
        if restart :
            reset_game()
            mainloop()
        
        if home_screen:
            menu()

#Main Menu
def menu():
    menu_run=True
    exit_menu=False
    while menu_run:
        screen.blit(background,(0,0))
        pygame.mixer.music.stop()
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                menu_run=False
        
        if start_button.draw(screen):
            menu_run=False
            exit_menu=True
        
        if help_button.draw(screen):
            help_screen()
        
        pygame.display.update()
    
    else:
        if exit_menu:
            reset_game()
            mainloop()

#Pause Screen
def pause_screen():
    global pause
    pygame.draw.rect(surface,(128,128,128,150),[0,0,width,height])
    screen.blit(surface,(0,0))
    screen.blit(options_image,(200,90))
    screen.blit(resume_image,(272,171))
    screen.blit(restart_image,(272,240))
    screen.blit(exit_image,(272,310))
    screen.blit(home_image,(310,370))

#Help screen
def help_screen():
    help_run=True
    while help_run:
        screen.fill("black")
        title_text=font.render("Controlls",True,"red")
        line1=font.render("1.Use Left Arraw key to Move Left",True,"white")
        line2=font.render("2.Use Right Arraw key to Move Right",True,"white")
        line3=font.render("3.Use Up Arraw key to Jump",True,"white")
        line4=font.render("4.Press Space key to Shoot Shurikens",True,"white")
        
        screen.blit(title_text,(280,30))
        screen.blit(line1,(40,100))
        screen.blit(line2,(40,160))
        screen.blit(line3,(40,220))
        screen.blit(line4,(40,280))
        if back_button.draw(screen):
            help_run=False
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                help_run=False
        
        pygame.display.update()

#Reset Game
def reset_game():
    global naruto_shurikens,N_throw_speed,sasuke_shurikens,S_throw_speed,naruto,sasuke
    naruto_shurikens=[]
    N_throw_speed=0
    sasuke_shurikens=[]
    S_throw_speed=0
    naruto=Player(600,400,100,100)
    sasuke=Enemy(30,400,100,100,600)

#Game over
def game_over(winner,color):
    global running
    
    screen.blit(gameover_image,(160,100))
    text=font.render(winner,True,color) 
    screen.blit(text,(260,150))
    
    if restart_button_1.draw(screen):
        running=False
        reset_game()
        mainloop()       
        
    if exit_button_1.draw(screen):
        running=False



#Call menu screen
menu()

pygame.quit()