import pygame
from settings import *

class Button():
    def __init__(self, display, x, y, POS, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.adj_x = x
        self.adj_y = y

        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.display = display
        self.font = pygame.font.SysFont(FONT[0], FONT[1])

        self.fillColors = INTERATION_COLORS

        #Ajustando retangulo de interação
        for rect in POS:
            self.adj_x += rect.x
            self.adj_y += rect.y

        self.button = pygame.Rect(self.x,self.y,self.width,self.height)
        self.button_click = pygame.Rect(self.adj_x,self.adj_y,self.width,self.height)
        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))



    def process(self):
        mousePos = pygame.mouse.get_pos()

        # Preenche a superfície do botão com a cor normal
        estado = 'normal'

        # Verifica se o mouse está sobre o botão
        if self.button_click.collidepoint(mousePos):
            estado = 'hover'  # Cor de hover
            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # Se o botão do mouse estiver pressionado
                estado = 'pressed'  # Cor quando pressionado
                if self.onePress:
                    self.onclickFunction()  # Chama a função de clique uma vez
                elif not self.alreadyPressed:
                    self.onclickFunction()  # Chama a função de clique
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        # Aqui você já desenha a superfície do botão (o retângulo + texto) na tela
        
        pygame.draw.rect(self.display, self.fillColors[estado], self.button)

        # Centraliza o texto no botão
        textRect = self.buttonSurf.get_rect(center=self.button.center)  # Centraliza o texto com base no centro do botão
        self.display.blit(self.buttonSurf, textRect)
