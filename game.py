from settings import *

class Game:
    def __init__(self):

        #general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
    
    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0), (x,self.surface.get_height()), 1 )
        
        for line in range(1 , ROWS):
            y = line * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)

    def run(self):
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING))