import pygame 
from overworld_sprite import Sprite

class Player(Sprite):
    def __init__(self, image_path, x, y): #Image_path er den vi selv vælger i overworld filen, og x og y er de led hvor spriten bevæger sig
        super().__init__(image_path, x, y) #Super kalder den overordnede klasse, som er sprite klassen, og kalder dens init funktion  #For collision detection, så der er en box omkring spriten
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.movement_speed = 2
        self.keys = pygame.key.get_pressed()
        self.channel = pygame.mixer.Channel(0)  
        self.step_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/step.mp3") 
        self.moving = False
    def update(self):
        self.old_x = self.x
        self.old_y = self.y
        self.keys = pygame.key.get_pressed()
        moving = self.keys[pygame.K_a] or self.keys[pygame.K_d] or self.keys[pygame.K_w] or self.keys[pygame.K_s]

        # If movement starts, play the footstep sound on loop; if stops, stop it.
        if moving and not self.moving:
            self.channel.play(self.step_snd, loops=-1)
            self.moving = True

        elif not moving and self.moving:
            self.channel.stop()
            self.moving = False
        
        if self.keys[pygame.K_a]:
            self.x -= self.movement_speed
            
        if self.keys[pygame.K_d]:
            self.x += self.movement_speed
            
            
        if self.keys[pygame.K_w]:
            self.y -= self.movement_speed
            
            
        if self.keys[pygame.K_s]:
            self.y += self.movement_speed
             
        self.rect.center = (self.x, self.y)
    def get_keys(self):
        return self.keys
       
    
       
         
   