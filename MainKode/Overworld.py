import pygame
import pygame.display
from overworld_player import Player
from overworld_sprite import sprites, Sprite
from button import Button
from level_sel import Levels
from asset import Asset
import requests
import os 
from complete import complete

class Overworld:
    def __init__(self):
        pygame.init()   
        pygame.display.set_caption("Overworld")
        self.asset = Asset(1280, 720)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.clear_color = (0, 0, 0)
        self.game_assets()
        self.level_1_collision = False
        self.level_2_collision = False
        self.level_3_collision = False
        self.level_4_collision = False  
        self.data_sent = False
        self.user_data = {
            "username" : os.environ.get("USERNAME", ""), #Brugernavnet fra
            "level_1" : 0,
            "level_2" : 0,
            "level_3" : 0,
            "level_4" : 0
        }
        

    def game_assets(self):
        sprites.clear() 
        self.level_enter = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/level_enter.mp3")
        self.player = Player("C:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/sprites/player/player_0.png", 112, 265)
        self.mainmusic = pygame.mixer.music.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/overworld.mp3")
        self.game_map = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/map.png")
        self.level_1 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/level_1.png")
        self.level_1_com = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/level_1_com.png")
        self.level_2 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/level_2.png")
        self.level_2_com = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/level_2_com.png")
        self.level_3 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/level_3.png")
        self.level_3_com = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/level_3_com.png")
        self.boss_closed = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/boss.mp3")
        self.boss_channel = pygame.mixer.Channel(0)
        self.level_2_rect = self.level_2.get_rect(center=(630, 550))
        self.level_3_rect= self.level_3.get_rect(center=(900, 450))
        self.level_4_com = self.asset.img("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/boss_com.png", 1175, 290, False)
        self.font = pygame.font.Font("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/font/overworld_font.ttf", 40)
        self.level1_text = self.font.render("1 - PHISHING", True, (255, 255, 255))
        self.level1_text_rect = self.level1_text.get_rect(center=(380, 290))
        self.level2_text = self.font.render("2 - GDPR", True, (255, 255, 255))
        self.level2_text_rect = self.level2_text.get_rect(center=(650, 450))
        self.level3_text = self.font.render("3 - PASSWORDS", True, (255, 255, 255))
        self.level3_text_rect = self.level3_text.get_rect(center=(900, 350))
        self.level4_text = self.font.render("4 - SIKKER SURFING", True, (255, 255, 255))
        self.level4_text_rect = self.level4_text.get_rect(center=(1000, 275))
        self.final_text = self.font.render("Gennemfør de 3 baner for at låse op for denne bane!", True, (255, 255, 255))
        self.final_text_rect = self.final_text.get_rect(center=(640, 680))
        self.space_text = self.font.render("Tryk SPACE", True, (255, 255, 255))
        self.space_text_rect = self.space_text.get_rect(center=(640, 680))
        self.level_1_rect = self.level_1.get_rect(center=(370, 390))
        self.level_1_col = self.level_1_rect.inflate(30, -150)  # Inflate the rect by 20 pixels in both directions
        self.game_map_rect = self.game_map.get_rect(topleft=(0,0)) 
        self.go_back = Button(image=None, pos=(150, 50), text_input="GO BACK", font=self.font, base_color="Red", hovering_color="White", hovering_image=None)
        self.level2_col = pygame.Rect(475, 400, 175, 175)
        self.level3_col = pygame.Rect(825, 400, 150, 150)
        self.level4_col = pygame.Rect(1000, 200, 150, 150)
        self.back_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/back_snd.mp3")
        self.frames_map = [pygame.image.load(f"c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/sprites/background/overworld_animation/map_{i}.png") for i in range(2)]

        pygame.display.flip()

    def user_progress(self):
        if complete.level_1_complete == True:
            self.user_data["level_1"] = 1
            self.data_sent = True
        if complete.level_2_complete == True:
            self.user_data["level_2"] = 1
        if complete.level_3_complete == True:
            self.user_data["level_3"] = 1
            print("level_3_complete")
        if complete.level_4_complete == True:
            self.user_data["level_4"] = 1
            print("level_4_complete")
        
        

    def collision_detection(self):
        self.levels = Levels()
        keys = self.player.get_keys()
        if self.level_1_col.colliderect(self.player.rect):
            self.level_1_collision = True
            if keys[pygame.K_SPACE]:
                pygame.mixer.music.stop()
                self.level_enter.play()
                self.levels.level_1()
        else:
            self.level_1_collision = False

        if self.level2_col.colliderect(self.player.rect):
            self.level_2_collision = True
            if keys[pygame.K_SPACE]:
                pygame.mixer.music.unload()
                self.level_enter.play()
                self.levels.level_2()
                     
        else:
            self.level_2_collision = False

        if self.level3_col.colliderect(self.player.rect): 
            self.level_3_collision = True 
            if keys[pygame.K_SPACE]:
                pygame.mixer.music.unload()
                self.level_enter.play()
                self.levels.level_3()
                
        else:
            self.level_3_collision = False

        if self.level4_col.colliderect(self.player.rect):
            self.level_4_collision = True
            if keys[pygame.K_SPACE]:
                self.boss_channel.play(self.boss_closed) #bug når man bevæger sig imens den spiller
                if self.boss_open == 3:
                    pygame.mixer.music.unload()
                    self.level_enter.play()
                    self.levels.level_4()
                    
        else:  
            self.level_4_collision = False

    def send_data(self):
        response = requests.post("https://cyberrila.com/api/submit", json=self.user_data)
        return response
    
    def load_data(self):
        self.load_url = "https://cyberrila.com/api/get_data?username=" + self.user_data["username"]
        try:
            self.response = requests.get(self.load_url)
            if self.response.status_code == 200:
                data = self.response.json()
                self.user_data["level_1"] = data.get("level_1", 0)
                self.user_data["level_2"] = data.get("level_2", 0)
                self.user_data["level_3"] = data.get("level_3", 0)
                self.user_data["level_4"] = data.get("level_4", 0)
                
                
        except requests.exceptions.RequestException as e:
            print(f"Error: connecting to server {e}")
      

    def draw(self):
        self.screen.fill(self.clear_color)  # Clear screen first
        self.current = self.frames_map[self.frame_index]
        self.screen.blit(self.current, (0, 0))
        pygame.draw.rect(self.game_map, (0,0,0), self.level2_col)
        pygame.draw.rect(self.game_map, (0,0,0), self.level3_col)  
        pygame.draw.rect(self.game_map, (0,0,0), self.level4_col)
        if self.user_data["level_1"] == 0:
            self.screen.blit(self.level_1, self.level_1_rect)
        else:
            self.screen.blit(self.level_1_com, self.level_1_rect)
        if self.user_data["level_2"] == 0:
            self.screen.blit(self.level_2, self.level_2_rect)
        else:
            self.screen.blit(self.level_2_com, self.level_2_rect) 
        if self.user_data["level_3"] == 0:
            self.screen.blit(self.level_3, self.level_3_rect)
        else:
            self.screen.blit(self.level_3_com, self.level_3_rect)
        if self.user_data["level_4"] == 0:
            self.level_4 = self.asset.img("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/boss.png", 1175, 290)
        else:
             self.level_4_com.place()
        
        if self.level_1_collision == True:
            self.screen.blit(self.level1_text, self.level1_text_rect)
            self.screen.blit(self.space_text, self.space_text_rect)
        if self.level_2_collision == True:
            self.screen.blit(self.level2_text, self.level2_text_rect)
            self.screen.blit(self.space_text, self.space_text_rect)
        if self.level_3_collision == True:
            self.screen.blit(self.level3_text, self.level3_text_rect)
            self.screen.blit(self.space_text, self.space_text_rect)
        if self.level_4_collision == True:
            if self.boss_open == 3:
                self.screen.blit(self.level4_text, self.level4_text_rect)
                self.screen.blit(self.space_text, self.space_text_rect)
            else:
                self.screen.blit(self.final_text, self.final_text_rect)
        for s in sprites:  # Draw all sprites
            s.draw(self.screen)

        
        # Check for collision with other sprites if needed
    def run(self):
        self.load_data()
        self.running = True
        self.frame_index = 0
        self.frame_delay = 35
        self.frame_counter = 0
        if self.running:
            pygame.mixer.music.play(-1, 0, 5000)  # Play background music 
        frame_counter = 0 
        while self.running:
            self.boss_open = self.user_data["level_1"] + self.user_data["level_2"] + self.user_data["level_3"]
            # update unlocked levels based on complete flags
            self.user_progress()
            

            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames_map)
                self.screen.blit(self.frames_map[self.frame_index], (0, 0))
            self.player_rect = self.player.rect
            self.mouse_pos = pygame.mouse.get_pos()
            self.collision_detection()
            
        # 1. Kigger efter events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    self.running = False
                # Exit overworld on ESC key press
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.go_back.checkForInput(self.mouse_pos):
                        pygame.display.set_caption("Main Menu")
                        self.back_snd.play()
                        pygame.mixer.music.unload()
                        self.running = False
              
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
            frame_counter += 1
            if frame_counter >= 300:
                self.send_data()
                frame_counter = 0

if __name__ == "__main__":
    overworld = Overworld()
    overworld.running = True
    overworld.run()