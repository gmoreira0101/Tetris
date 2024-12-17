from settings import *
from button import Button
class Pause:
    def __init__(self):
        self.surface = pygame.Surface((PAUSE_WIDTH, PAUSE_HEIGHT))
        self.rect = self.surface.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface = pygame.display.get_surface()


        self.buttons_surface = pygame.Surface((PAUSE_WIDTH*PAUSE_BUTTONS_PROPORTION,PAUSE_HEIGHT*PAUSE_BUTTONS_PROPORTION))
        self.rect_button = self.buttons_surface.get_rect(center = (PAUSE_WIDTH // 2, PAUSE_HEIGHT // 2))

        self.buttons = []

    def draw_buttons(self):


        def teste():
            print('teste')

        #Criando Botões
        for i,tipo in enumerate(NOME_BOTAO):
            
            width = PAUSE_WIDTH*PAUSE_BUTTONS_PROPORTION - 2*PADDING
            height = (PAUSE_HEIGHT*PAUSE_BUTTONS_PROPORTION - 4*PADDING)/3

            x = PADDING
            y = PADDING + i*(height+PADDING)
            tmp = Button(self.buttons_surface,x,y,width,height, tipo ,teste)
            self.buttons.append(tmp)

            

    
        for button in self.buttons:
            button.process()

        self.surface.blit(self.buttons_surface, self.rect_button)
        self.buttons_surface.fill((0,0,0))

    def run(self):
        self.surface.fill(GRAY)
        self.draw_buttons()
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)