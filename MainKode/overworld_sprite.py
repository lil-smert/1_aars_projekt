import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image_path, x, y):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        loaded[image_path] = self.image
        self.x = x
        self.y = y
        sprites.append(self) # Spriten tilføjes til listen af sprites, så den kan tegnes på skærmen
    
    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
