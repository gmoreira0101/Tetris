from settings import *
from random import choice

class Game:
    def __init__(self):

        #general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))

        #Lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # tetromino
        self.tetrmino = Tetronimo(choice(list(TETROMINOS.keys())), self.sprites)

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x,self.surface.get_height()), 1 )
        
        for line in range(1 , ROWS):
            y = line * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)
        
        self.surface.blit(self.line_surface, (0,0))

    def run(self):

        #drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Tetronimo:
    def __init__(self, shape, group):
        #setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        #create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        
        #general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
       
        #position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft = (x,y))