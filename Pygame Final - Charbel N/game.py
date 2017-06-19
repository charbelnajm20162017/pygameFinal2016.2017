import pygame
import config
import sys
import os
pygame.init()
screen = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption("Pygame Final - Charbel Najm")
clock = pygame.time.Clock()
pygame.mixer.init()

groundColliders = pygame.sprite.Group()
all_colliders = pygame.sprite.Group()

# Ground collider class
class ground(pygame.sprite.Sprite):
    def __init__(self, color, width, height, rectx, recty):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.image.set_alpha(0) #for debugging
        self.rect.x = rectx
        self.rect.y = recty
        groundColliders.add(self)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):     
        super().__init__()
        self.image = pygame.image.load("resources/king1/king1_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, ((15*2,22*2)))
        self.rect = self.image.get_rect()
        all_colliders.add(self)
        
#Main Game Class
class GameRun(object):
    def __init__(self, w, h):
        self.dw = w
        self.dh = h
        self.screen = pygame.display.set_mode((w, h))
        self.run()

    def run(self):
        running = True
        pygame.key.set_repeat()

        ## used for moving the player
        i = [200, 1]
        
        speedX = 6
        speedY = 6
        kX, kY = 0, 0
        kRight, kLeft, kUp, kDown = False, False, False, False        
                
        player = Player()
        global jumping
        global yVel
        global level
        jumping = True
        gravity = 1.4
        yVel = 0
        level = 0

        ##

        # Jump handling
        def jump(height=-15, grounded=False):
            global jumping
            global yVel
            if jumping == False or grounded == True:
                yVel = height
                if jumping == False:
                    jumping = True

        # Switches to the next level
        def nextLevel(lvl):
            if lvl == 0:
                level = 1
                return level
            if lvl == 1:
                level = 2
                return level
            if lvl == 2:
                level = 3
                return level
        pygame.mixer.music.load("resources/b423b42.wav")
        pygame.mixer.music.play(-1)
        
        # Main Loop
        while running == True:
            if level == 0:
                #Load intro screen
                bg = pygame.image.load("resources/worlds/world0-600x480-intro.png").convert()
                #Draw colliders
                groundColliders.empty()
                g = ground(config.RED, config.width, 7, 0, 460)
            if level == 1:
                #Load level 1
                bg = pygame.image.load("resources/worlds/world1-600x480.png").convert()            
                #Draw colliders
                groundColliders.empty()
                g = ground(config.RED, 350, 7, 0, 340)
                g2 = ground(config.RED, 135, 7, config.width-135, 340)
                g3 = ground(config.RED, 15, 15, config.width-63, 306)
                g4 = ground(config.RED, 15, 15, config.width-72, 322)
                g5 = ground(config.RED, 15, 15, config.width-46, 322)
            if level == 2:
                #Load level 2
                bg = pygame.image.load("resources/worlds/world2-600x480.png").convert()
                #Draw colliders
                groundColliders.empty()
                g = ground(config.RED, 165, 7, 0, 350)
                g2 = ground(config.RED, 50, 7, 185, 280)
                g2 = ground(config.RED, 50, 7, 290, 230)
                g3 = ground(config.RED, config.width - 380, 7, 380, 350)
            if level == 3:
                #Load level 3 and keep colliders from level 2
                bg = pygame.image.load("resources/worlds/world2-END-600x480.png").convert()            
            
            #Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if level == 0:
                            level = nextLevel(level)
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("resources/Harp.ogg")
                            pygame.mixer.music.play(-1)
                    if event.key == pygame.K_RIGHT:
                        kRight = True
                    if event.key == pygame.K_LEFT:
                        kLeft = True           
                    if event.key == pygame.K_UP:
                        kUp = True                             
                    if event.key == pygame.K_DOWN:
                        kDown = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        kRight = False
                    if event.key == pygame.K_LEFT:
                        kLeft = False           
                    if event.key == pygame.K_UP:
                        kUp = False                             
                    if event.key == pygame.K_DOWN:
                        kDown = False

            # Reset player's position if falling out of level
            if player.rect.y >= 599:
                player.rect.x, player.rect.y = 10, 10
                
            # Detect if the player has reached the end of the level
            if player.rect.x >= config.width - 50 and level != 0:
                print("next level")
                level = nextLevel(level)
                player.rect.x, player.rect.y = 10, 10
                
            # Collision Handling
            hit = pygame.sprite.spritecollide(player, groundColliders, False)
            #print(hit) #debugging

            # Movement handling
            if kRight:
                player.rect.x += speedX
            elif kLeft:
                player.rect.x -= speedX
            if kUp:
                # if len(hit) != 0 : If the player is colliding with anything
                if len(hit) != 0:
                    #move player slightly upwards to allow the jump to be smooth
                    player.rect.y -= 7
                # If not already jumping, jump. This sets a 1 jump limit until the player touches a collider again.
                if jumping != True:
                    yVel = -15
                    jumping = True
            # Gravity
            if len(hit) == 0:
                yVel += gravity
            else:
                # Remove any stored yVelocity if player is touching a collider
                yVel = 0
                jumping = False
                
            player.rect.y += yVel
            
            self.screen.blit(bg, bg.get_rect())
            all_colliders.draw(self.screen)
            groundColliders.draw(self.screen)

            #debugging
            #def drawRect(color, x,y,width,height,w2=0):
            #    pygame.draw.rect(self.screen, color, (x,y,width,height), w2)
            
            ## extra
            #drawRect(config.GREEN, 150, 425, 20,20)
            #if player.rect.x == 150:
            #    jump(-25)
            ##

            # Movement Handling
            # Horizontal movement
            if i[0] <= 0: i[1] = 0
            if i[0] >= 201: i[1] = 1
            
            #update clock and display
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    GameRun(config.width, config.height)

    

