import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
# In Teris we have a 10 by 20 grid, so set the play_width  = 0.5 * play_height
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# the top_left position of the actual play area
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
# represent the shapes in Teris
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (75, 136, 201), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    rows = 20   # y
    columns = 10    # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0   # num 0 - 3

# create one list for every row in the grid (20 sublist)
# for each sublist we have 10 color.
def create_grid(locked_positions={}):
    # (0, 0, 0): black
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    # also check the static grids
    for i in range(len(grid)):  # 20 rows
        for j in range(len(grid[i])):   # 10 cols
            if (j, i) in locked_positions:  # key exist in locked_position
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

# convert the shape
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] # give us the sublist that we need

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # shape.x the current value of teh shape
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # remove teh offset left and up

    return positions

def valid_space(shape, grid):
    # every possible position in a 10 * 20 grid
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # flatten the list
    accepted_pos = [j for sub in accepted_pos for j in sub] # [(), ()]

    # convert shape to format
    formatted = convert_shape_format(shape) #[(), ()]

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1 :
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:   # touch the top, you loss
            return True
    return False

# Randomly pick one shape from the shapes list.
def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2,
                         top_left_y + play_height / 2 - label.get_height() / 2))


# draw the line for the gird
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        # for ever row draw a line
        pygame.draw.line(surface, (128, 128, 128),
                         (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128),
                             (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0 # an increment

    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i # index
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        # sort the locked based on the y value of the locked dictionary
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind: # if y is above the current index we removed
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc  # return the number of rows we clear


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicisans', 30)
    label = font.render('Next shape:', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))



def draw_window(surface, gird, score = 0, last_score = 0):
    surface.fill((0, 0, 0))
    # draw a title
    pygame.font.init()  # init font object, we are ready to draw on the screen
    # create a font
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Teris', 1, (255, 255, 255)) # white font
    # draw the label on the screen (in the middle)
    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    # current score-----------------------------------------------------
    font = pygame.font.SysFont('comicisans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 30, sy + 160))
    # -------------------------------------------------------------------
    # last score --------------------------------------------------------
    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 30, sy + 160))
    # -------------------------------------------------------------------

    # now draw the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size,
                              block_size, block_size), 0)
    # red rectangle
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

# update the score in scores.txt
def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def main(win):

    last_score = max_score()

    global grid

    locked_positions = {}   # position: color value  e.g: {(1, 2): (255, 0, 0)}

    # create grid
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape() # get a random shape
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27 # how long it will take before each shape starts falling
    level_time = 0  # how much time has passed, we increase the speed as time passes
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()    # get the time interval between last clock.tick()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 10 :  # every 10 second we increase the speed
            level_time = 0
            if fall_speed > 0.12:   # stop increasing speed if fall_speed is too fast
                fall_speed -= 0.005


        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1    # move our piece down
            if not (valid_space(current_piece, grid)) and (current_piece.y > 0):
                current_piece.y -= 1    # we are in a invalid position, so move back
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # left arrow
                    # move our block left
                    current_piece.x -= 1
                    # check if it is a valid position
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:     # right arrow
                    # move block right
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:  # down arrow
                    # move down
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:    # up arrow
                    # rotate the shape
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece) # check all the positions of the piece moving down,
                                                        # see if we hit the ground (then we need to lock it).

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # if piece hit the ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        # draw the grid
        draw_window(win, grid, score, last_score)

        # draw the next shape
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # check if we lost the game
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

# create a pygame surface
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
