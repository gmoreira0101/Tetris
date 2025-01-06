from settings import *
from sys import exit
from game import Game
from score import Score
from preview import Preview
from pause import Pause
from os import path
import os

import random


def generate_next_shapes(num_shapes, exclude_shape = None):
    shapes = list(TETROMINOS.keys())
    
    if exclude_shape and exclude_shape in shapes:
        shapes.remove(exclude_shape)
    
    next_shapes = []
    
    for _ in range(num_shapes):
        shape = random.choice(shapes)
        while next_shapes and shape == next_shapes[-1]:
            shape = random.choice(shapes)
        next_shapes.append(shape)
    
    return next_shapes
class Main:
    def __init__(self):
        
        #General
        self.restart = False
        self.quit = False

        #Configurando posicionamento da tela
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_X_POS,WINDOW_Y_POS)
        pygame.init()

        #Criando interface display
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.NOFRAME)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        # Lista inicial aleatória
        self.next_shapes = generate_next_shapes(3)

        #components
        self.game = Game(self.get_next_shape, self.update_score, self.start_song)
        self.score = Score()
        self.preview = Preview()
        self.pause = Pause(self, self.game)


    def start_song(self, setting = 1):

        if setting == 1:
            pygame.mixer.init()
            
            self.background_music = pygame.mixer.music.load(path.join('musics','TetrisSong.mp3'))
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        elif setting == 0:
            pygame.mixer.music.pause()
        elif setting == -1:
            pygame.mixer.music.unpause()

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    
    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(generate_next_shapes(1, self.next_shapes[1])[0])
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
                self.next_shapes = generate_next_shapes(3)
                self.game = Game(self.get_next_shape, self.update_score, self.start_song)
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