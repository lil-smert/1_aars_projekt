import pygame, sys
from button import Button
import pygame.display
from cryptography.fernet import Fernet
import os
import requests
from asset import Asset
# Gøre password usynligt, gør login knap flottere, gør boxes større, shift/enter når man indtaster

class Login:
    def get_font(self, size):  # Import font with specified size
        return pygame.font.Font("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/font/menufont.otf", size)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.asset = Asset(1280, 720)
        self.clock = pygame.time.Clock()
        self.login_box = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/loginbox.png")
        self.login_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/login.mp3")
        self.login_error_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/login_error.mp3")
        pygame.display.set_caption("Login Menu")
        self.menu_font = self.get_font(32)
        self.font ="c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/font/menufont.otf"
        # Konstante variabler, som ikke skal ændres
        self.login_success = False
        self.user_text1 = ''
        self.user_text2 = '' #bcrypt opererer med bytes, øger sikkerheden
        self.username_state = False
        self.password_state = False
        self.cred_error = False
        self.rect_color_active = pygame.Color('lightskyblue3')
        self.rect_color_pas = pygame.Color('gray15')
        self.color1 = self.rect_color_pas
        self.color2 = self.rect_color_pas
    def login_auth(self):
        if self.login_button.checkForInput(self.menu_mouse_pos): #Sender API-request til server
                    self.url = "https://cyberrila.com/api/login"
                    try:
                        self.response = requests.post(self.url, json={"username": self.user_text1, "password": self.user_text2}, allow_redirects=False)
                    except requests.exceptions.RequestException as e:
                        print(f"Error: connecting to server {e}")
                        self.login_error_snd.play()
                        return
                    
                    if self.response.status_code == 200: 
                        os.environ["USERNAME"] = self.user_text1 #Gemmer brugernavnet, så vi kan bruge det i andre klasser
                        self.login_success = True
                        self.login_snd.play()
                        self.cred_error = False
                    else:
                        self.login_error_snd.play()
                        self.cred_error = True
                        

    def login_input(self):
        # Draw username and password input fields
        self.username_rect = pygame.Rect(840, 400, 240, 45)
        self.password_rect = pygame.Rect(840, 550, 240, 45)

        self.username_text = self.get_font(30).render("Username:", True, "White")
        self.password_text = self.get_font(30).render("Password:", True, "White")
        self.username_text_place = self.username_text.get_rect(center=(920, 370))
        self.password_text_place = self.password_text.get_rect(center=(920, 520))

        self.screen.blit(self.username_text, self.username_text_place)
        self.screen.blit(self.password_text, self.password_text_place)

        # Draw username input box
        pygame.draw.rect(self.screen, self.color1, self.username_rect, 3)
        text_surface1 = self.menu_font.render(self.user_text1, True, (255, 255, 255))
        self.screen.blit(text_surface1, (self.username_rect.x + 5, self.username_rect.y + 5))
        self.username_rect.w = max(300, text_surface1.get_width() + 10)

        # Draw password input box
        pygame.draw.rect(self.screen, self.color2, self.password_rect, 3)
        text_surface2 = self.menu_font.render(self.user_text2, True, (255, 255, 255))
        self.screen.blit(text_surface2, (self.password_rect.x + 5, self.password_rect.y + 5))
        self.password_rect.w = max(300, text_surface2.get_width() + 10)

        # Update colors based on active state
        self.color1 = self.rect_color_active if self.username_state else self.rect_color_pas
        self.color2 = self.rect_color_active if self.password_state else self.rect_color_pas

        self.menu_logo = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/logo.png") # Vi laver logo til menuen
        self.menu_place = self.menu_logo.get_rect(center=(950, 240))
        self.screen.blit(self.menu_logo, self.menu_place) # Vi placerer logoet
    def handle_events(self):
        self.menu_mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if username or password fields are clicked
                self.username_state = self.username_rect.collidepoint(event.pos)
                self.password_state = self.password_rect.collidepoint(event.pos)

                # Check if login button is clicked
                if self.login_button.checkForInput(self.menu_mouse_pos):
                    self.login_auth()

            if event.type == pygame.KEYDOWN:
                # Handle text input for username
                if self.username_state:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text1 = self.user_text1[:-1]
                    else:
                        self.user_text1 += event.unicode

                # Handle text input for password
                if self.password_state:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text2 = self.user_text2[:-1]
                    else:
                        self.user_text2 += event.unicode

    def login_func(self):
        # Draw login button
        self.login_button = Button(image=None, pos=(960, 680), text_input="LOGIN", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        self.login_button.changeColor(self.menu_mouse_pos)
        self.login_button.update(self.screen)

        # Display error message if credentials are wrong
        if self.cred_error:
            wrong_text = self.get_font(30).render("Wrong Credentials!", True, "Red")
            wrong_text_place = wrong_text.get_rect(center=(960, 780))
            self.screen.blit(wrong_text, wrong_text_place)

    def run(self):
        while not self.login_success:
            self.screen.fill((0, 0, 0))  # Clear screen first

            self.menu_mouse_pos = pygame.mouse.get_pos()
            self.handle_events()         # Handle input/events

            self.login_input()           # Draw input fields and text
            self.login_func()            # Draw login button and error message

            pygame.display.flip()        # Update the display
            self.clock.tick(60)


if __name__ == "__main__":
    login = Login()
    login.run()