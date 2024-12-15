from settings import *
from random import choice

from timer import Timer

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
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

        #timer
        self.timers = {
            'vertical move'         : Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move right' : Timer(MOVE_WAIT_TIME),
            'horizontal move left'  : Timer(MOVE_WAIT_TIME),
            'vertical move input'   : Timer(MOVE_WAIT_TIME),
            'rotate'                : Timer(ROTATE_WAIT_TIME)  
        }
        self.timers['vertical move'].activate()
    
    def create_new_tetromino(self):
        
        #kill completed rows
        self.check_fineshed_rows()
        
        #create new tetromino
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down(1)

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x,self.surface.get_height()), 1 )
        
        for line in range(1 , ROWS):
            y = line * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)
        
        self.surface.blit(self.line_surface, (0,0))

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['horizontal move left'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move left'].activate()
        
        if not self.timers['horizontal move right'].active:
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move right'].activate()
        
        if not self.timers['vertical move input'].active:
            if keys[pygame.K_DOWN]:
                self.tetromino.move_down(1)
                self.timers['vertical move input'].activate()
        
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()
    
    def check_fineshed_rows(self):

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

    def run(self):

        #update
        self.input()
        self.timer_update()
        self.sprites.update()

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