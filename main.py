from settings import *
from sys import exit
from game import Game
from score import Score
from preview import Preview
from pause import Pause

from random import choice

class Main:
    def __init__(self):
        
        #General
        self.restart = False
        self.quit = False
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        #shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        #components
        self.game = Game(self.get_next_shape)
        self.score = Score()
        self.preview = Preview()
        self.pause = Pause(self, self.game)

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape
    
    def run(self):
        while not self.quit:
            for event in pygame.event.get():
                if event.type  == pygame.QUIT or self.quit:
                    pygame.quit()
                    exit()
            if self.restart:
                #Reiniciando componentes
                self.restart = False
                self.game = Game(self.get_next_shape)
                self.score = Score()
                self.preview = Preview()
                self.pause = Pause(self, self.game)
            #Display
            self.display_surface.fill(GRAY)
            
            self.game.run(self.game.pause_status)
            self.score.run()
            self.preview.run(self.next_shapes)

            if self.game.pause_status:
                self.pause.run()
            
             
            #updating the game
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    main = Main()
    main.run()