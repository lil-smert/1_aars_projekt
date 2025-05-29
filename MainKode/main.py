import pygame, sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Minigame 4')

        self.current_stage = Level()

    def run(self):
        running = True
        while running:
            running = self.current_stage.run()
            # display update handled inside Level.run()
        return running

if __name__ == '__main__':
    try:
        game = Game()
        game.run()

    except Exception as e:
        print("Error:", e)
        import traceback; traceback.print_exc()
        pygame.quit()
        sys.exit()

