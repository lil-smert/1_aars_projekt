import pygame
from overworld_player import Player
from overworld_sprite import sprites, Sprite
from Overworld import Overworld
from button import Button
from asset1 import Asset

class map_intro:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.clear_color = (0, 0, 0)
        self.game_assets()
        self.next_scene = None
    
    def game_assets(self):
        sprites.clear() 
        self.player = Player("C:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/sprites/player/player_0.png", 480, 250)
        self.game_map = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/hq_map.png")
        self.game_map_rect = self.game_map.get_rect(center=(640, 360))
        self.menu_rect = pygame.Rect(300, 670, 250, 150)
        self.go_back = Button(image=None, pos=(150, 50), text_input="GO BACK", font=pygame.font.Font(None, 75), base_color="Red", hovering_color="White", hovering_image=None)
        self.back_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/back_snd.mp3")
        pygame.mixer.music.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/overworld.mp3")
        pygame.display.flip()
    def collision_detection(self):
        keys = self.player.get_keys()
        if self.menu_rect.colliderect(self.player.rect):
            self.player.x = self.player.old_x
            self.player.y = self.player.old_y
            pygame.mixer.music.unload()
            self.running = False
            self.next_scene = "overworld"
                
    def draw(self):
        pygame.draw.rect(self.screen, (0,0,0), self.menu_rect)
        self.screen.fill(self.clear_color)  # Clear screen first
        self.screen.blit(self.game_map, self.game_map_rect)
        Asset.img(self, "c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/arrow.png", 450, 650, self.screen)
        for s in sprites:  # Draw all sprites
            s.draw(self.screen)
    def run(self):
        pygame.mixer.music.play(-1, 0, 5000)  # Play background music
        while self.running:
            self.player_rect = self.player.rect
            self.mouse_pos = pygame.mouse.get_pos()
            self.collision_detection()
        # 1. Kigger efter events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.go_back.checkForInput(self.mouse_pos):
                        self.screen.fill((0, 0, 0))
                        self.running = False
                        pygame.display.set_caption("Main Menu")
                        self.back_snd.play()
                        
              
            for button in [self.go_back]:
                button.changeColor(self.mouse_pos)
        
        # 2. Tjekker for input
            self.player.update()
        # 3. Draw everything
            self.draw()
            self.go_back.update(self.screen)
        
        # 4. Update display once per frame
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    intro_map = map_intro()
    intro_map.run()
    