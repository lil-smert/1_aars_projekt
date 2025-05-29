import pygame, sys
import pygame.display
from button import Button  # Importer knap klassen fra button.py
import sqlite3
import login
from intro_map import map_intro
from Overworld import Overworld
from asset import Asset
import random
#Gør fact box pænere
pygame.init()
asset = Asset(1280, 720) # Vi laver en instans af asset klassen, som er vores baggrund
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN) # Vi laver et vindue til vores spil
pygame.mixer.music.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/menu.mp3") # Vi importerer musikken til menuen # Bliver afspillet i starten
menu_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/menusnd.mp3")
menu_play_snd = pygame.mixer.Sound("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/music/menu_play.mp3")
clock = pygame.time.Clock()
login = login.Login()
frames = [pygame.image.load(f"c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/sprites/background/menu_animation/background_{i}.gif") for i in range(20)]
background = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/sprites/background/menu_animation/background_0.gif") # Vi importerer baggrunden til menuen
play_img = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/play_btn.png")
play_img2 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/play_btn2.png")
options_img1 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/options_1.png")
options_img2 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/options_2.png")
exit_img1 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/exit_1.png") # Vi importerer billederne til knapperne
exit_img2 = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/exit_2.png")
pygame.display.set_caption("Main Menu")
font = "c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/font/menufont.otf"

def get_font(size):  # Vi importerer fontenlogi, og "size" er størrelsen på fonten, som vi så definerer senere
    return pygame.font.Font("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/font/menufont.otf", size)
play_button = Button(image=play_img, pos=(225, 600), text_input="", font=get_font(100), base_color="#d7fcd4", hovering_color="White", hovering_image=play_img2)
options_button = Button(image=options_img1, pos=(650, 600), text_input="", font=get_font(100), base_color="#d7fcd4", hovering_color="White", hovering_image=options_img2) # Vi laver en knap til options menuen
exit_button = Button(image=exit_img1, pos=(1075, 600), text_input="", font=get_font(100), base_color="#d7fcd4", hovering_color="White", hovering_image=exit_img2) #
fact_img = pygame.image.load("c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/pictures/fact.png") # Vi importerer billedet til facts knappen
fact_rect = fact_img.get_rect(center=(625, 250)) # Vi laver en rektangel til facts knappen
pygame.display.flip() # Vi opdaterer skærmen

 # Vi placerer billedet på skærmen
menu_font = get_font(32) # Vi definerer fonten til 32, som er standard fonten
clock.tick(60)

fact_dict = {
        "fact_1": "Cirka 90 procent af alle cyberangreb starter med en phishing mail",
        "fact_2": "Menneskefejl er den primære årsag bag cyberangreb",
        "fact_3": "Over halvdelen af ansatte klikker på links i phishing-mails",
    }

def options():
    pygame.display.set_caption("Options")
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        options_back = Button(image=None,text_input="Go Back", pos=(640, 650), font=get_font(75), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        options_back.changeColor(options_mouse_pos)
        options_game_snd = Button(image=None,text_input="Game Volume", pos=(640, 450), font=get_font(75), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        options_game_snd.changeColor(options_mouse_pos)
        options_back.update(screen)
        options_game_snd.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    menu_snd.play()
                    main_menu()
                if options_game_snd.checkForInput(options_mouse_pos):
                    menu_snd.play()
                    main_menu()
        pygame.display.update()

def redrawWindow(): # Vi laver en funktion til at opdatere vinduet
    screen.fill((0, 0, 0)) # Vi fylder skærmen med sort
    screen.blit(background, (0, 0)) # Vi tilføjer baggrunden til skærmen
    
    
def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)

def main_menu(): # Vi spiller musikken i loop
    frame_index = 0
    frame_delay = 5
    frame_counter = 0
    fact_slide = 3
    current_fact = ""
    fact_timer = 0
    fact_delay = 5000
    fact_ready = False
    while True:
        dt = clock.tick(60) # Vi sætter fps til 60
        fact_timer += dt # Vi tilføjer tiden til faktatimeren

        frame_counter += 1
        if frame_counter >= frame_delay:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(frames)
            screen.blit(frames[frame_index], (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos() # Vi laver en variabel til musens position
        screen.blit(fact_img, fact_rect) # Vi tilføjer billedet til skærmen
        
        if (fact_timer > fact_delay or current_fact == ""):
            random_fact = random.choice(list(fact_dict.keys()))
            fact_ready
            current_fact = fact_dict[random_fact]
            fact_timer = 0  # Reset timer
            fact_ready = True
            
        if fact_ready:
            asset.font(current_fact, "c:/Users/vikto/Desktop/KEA/Projekt/Pygame/assets/font/menufont.otf", 
                      26, 175, 225, (0,0,0))
        
        
        for button in [play_button, options_button, exit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos): # Vi kalder fade funktionen, som vi definerer senere
                    menu_play_snd.play()
                    pygame.mixer.music.stop()
                    pygame.display.set_caption("Cyberilla HQ")
                    fade(1920, 1080)
                    intro = map_intro()
                    intro.run() # Vi laver en instans af overworld klassen, som er vores spil
                    if intro.next_scene == "overworld":
                        overworld = Overworld()
                        overworld.run()
    
                    print("Play button pressed")
                    # Add code to start the game here
                if options_button.checkForInput(menu_mouse_pos):
                    menu_snd.play()
                    options()
                if exit_button.checkForInput(menu_mouse_pos):
                    menu_snd.play()
                    pygame.quit()
                    sys.exit()
            
            

        pygame.display.flip()

login.run() # Kør login klassen, som er login skærmen
if login.login_success == True:
    pygame.mixer.music.play(-1)
    main_menu()

