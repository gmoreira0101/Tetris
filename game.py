from settings import *
from random import choice

from timer import Timer

class Game:
    def __init__(self, get_next_shape, update_score, song):

        #general
        self.song = song
        self.pause_status = False
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.endgame = False

        #game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        #Lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # starting song
        self.song(1)

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

        #timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move'         : Timer(self.down_speed, True, self.move_down),
            'horizontal move right' : Timer(MOVE_WAIT_TIME),
            'horizontal move left'  : Timer(MOVE_WAIT_TIME),
            'vertical move input'   : Timer(MOVE_WAIT_TIME),
            'rotate'                : Timer(ROTATE_WAIT_TIME),  
        }
        self.timers['vertical move'].activate()

        self.timer_pause = {
            'pause'                 : Timer(PAUSE_WAIT_TIME)
            }

        #score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0


    def calculate_score(self, num_lines):
        print(num_lines)
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level  

        #every 10 lines += level by 1
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].durantion = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def create_new_tetromino(self):
        
        #kill completed rows
        self.check_fineshed_rows()
        
        #create new tetromino
        self.tetromino = Tetromino(
            self.get_next_shape(), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down(1)

    def pause(self):
        self.pause_status = not self.pause_status

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x,self.surface.get_height()), 1 )
        
        for line in range(1 , ROWS):
            y = line * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)
        
        self.surface.blit(self.line_surface, (0,0))

    def input(self):

        #Pressionando teclado
        keys = pygame.key.get_pressed()
        if not self.timers['horizontal move left'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move left'].activate()
        
        if not self.timers['horizontal move right'].active:
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move right'].activate()
        
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster
            print('pressing down')
        
        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed
            print('releasing down')
        
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()
        
        if not self.timer_pause['pause'].active:
            if keys[pygame.K_ESCAPE]:
                self.pause()
                self.timer_pause['pause'].activate()
    
    def check_fineshed_rows(self):
        # Check if any block surpassed the screen vertically
        for row in self.field_data:
            for block in row:
                if block and (block.pos.y < 0 or block.pos.y >= ROWS):  # Verifica se o bloco ultrapassou os limites verticais
                    self.endgame = True
                    print("Game Over! Um bloco ultrapassou os limites verticais.")
                    return  # Finaliza a função assim que detectar o erro
        #get the full row indexes
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)
        
        if delete_rows:
            for delete_row in delete_rows:

               #delete full row
                for block in self.field_data[delete_row]:
                   block.kill()

                #move down the blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                           block.pos.y += 1
            
            # rebuild the field data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            #update score
            self.calculate_score(len(delete_rows))


    def run(self, pause = False):

        #update
        self.input()
        self.timer_pause['pause'].update()
        if not pause:
            self.timer_update()
            self.sprites.update()
            self.song(-1)
        else:
            self.song(0)

        #drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        #setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        #create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

        #collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    
    def next_move_vertical_collide(self, blocks, amount):
        collistion_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collistion_list) else False

    def move_down(self, amount):
        if not self.next_move_vertical_collide(self.blocks, amount):
            for blocks in self.blocks:
                blocks.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for blocks in self.blocks:
                blocks.pos.x += amount
    
    def rotate(self):
        if self.shape != 'O':
            
            #pivot point
            pivot_pos = self.blocks[0].pos
            
            # new block position
            new_block_position = [block.rotate(pivot_pos) for block in self.blocks]

            #collision check
            for pos in new_block_position:
                if pos.x < 0 or pos.x >= COLUMNS:
                    return
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
                if pos.y > ROWS:
                    return
            #implement new positions
            for i, block in enumerate(self.blocks):
                block.pos = new_block_position[i]

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

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)


    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
    
    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True
    def vertical_collide(self, y, field_data):
        if not y < ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True