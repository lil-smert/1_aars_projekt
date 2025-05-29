import pygame

### Path er billedepath som sting, x og y er placering af billedet, screen er display, og place er hvis du vil placerer det med det samme skriver du ingenting i place
### og hvis du vil placere det senere så sætter du den til false når du kalder klassen
# Når du kalder din asset i koden, skal du fastsætte skærmstørrelsen f.eks. asset = Asset(1280, 720), dette gør så du ikke skal skrive det ind hver gang
class Asset:
    def __init__(self):
        pass

    def img(self, path, x, y, screen, place=True):
        self.image = pygame.image.load(path)
        self.rect_img = self.image.get_rect(center=(x, y))
        if place == True:
            screen.blit(self.image, self.rect_img)
        else:
            pass
        return self
    
    def font(self, text, font, size, x, y, screen, color=(0,0,0), place=True):
        self._font = pygame.font.Font(font, size)
        self.text = self._font.render(text, True, color)
        if place == True:
            screen.blit(self.text, (x, y))
        else:
            pass

    def rect(self, x, y, width, height, screen, color=(0,0,0), place = True):
        self.rect = pygame.Rect(x, y, width, height)
        if place == True:
            self.draw_rect = pygame.draw.rect(screen, color, self.rect)
        else:
            pass

    #Hvis man ønsker at placere det senere, når man kalder funktionen skal man ændre place til False
    def place(self, screen):
        screen.blit(self.image, self.rect_img)

    def place_text(self, x, y, screen):
        screen.blit(self.text, (x, y) )

    def place_rect(self):
        self.draw_rect = pygame.draw.rect(self.screen, (0,0,0), self.rect)
    
    def remove(self):
        self.rect_img = self.image.get_rect(center=(10000, 10000))
    
    def collision(self):
        self.image.get_rect(center=(self.x, self.y))