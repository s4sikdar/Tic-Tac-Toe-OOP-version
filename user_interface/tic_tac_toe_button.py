import pygame
import sys
import math

pygame.init()
width = 700
height = 700
diameter = 200
timer = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))

square_to_draw = pygame.Rect(((width - diameter) / 2),
                             ((height - diameter) / 2),
                             diameter, diameter)
drawing_seconds = 0.5
black = (0, 0, 0)
white = (255, 255, 255)
FPS = 60
width = 10

drawing_area = {
    "top": 250,
    "left": 250,
    "right": 450,
    "bottom": 450
}
circle_drawn = False

class TicTacToeButton:
    def __init__(self, line_width, margin, drawing_seconds, color, start, edge_length):
        '''
            This is the class that represents a single button that is
            clicked to draw either an X or an O. The button is
            represened by an outline of a square, and the inside of the
            square is where the figure will be drawn. The constructor takes
            the following parameters:
            line_width: the width we use to draw a line
            margin: the margin between the drawn figure, and the outline of the
            button
            drawing_seconds: the number of milliseconds taken to draw the figure
            color: the color used to draw the figure
            start: the (x, y) coordinates for the top-left of the region where the
            figure will be drawn
            edge_length: since the region in which the figure will be drawn is a
            square, the edge length refers to the length of an edge on the square.
            This will be combined with the parameter start to determine the (x, y)
            coordinates of the bottom-right of the region where the figure will
            be drawn.
        '''
        self.figure_drawn = False
        self.start_time = None
        self.draw_circle = True
        self.line_width = line_width
        self.margin = margin
        self.drawing_seconds = drawing_seconds
        self.color = color
        self.drawing_area = {
            "top": start[1],
            "left": start[0],
            "right": start[0] + edge_length,
            "bottom": start[1] + edge_length
        }

    def switch_figure(self, value=None):
        '''
            self.switch_figure(value) switches the value of self.draw_circle
            to value if value is not None, False, or any equivalent value that
            translates to a False boolean value. Otherwise, self.draw_circle
            is equal to its boolean negation. self.draw_circle represents
            whether we draw an O or an X.
            switch_figure: TicTacToeButton (Anyof Bool None) -> None
        '''
        self.draw_circle = not self.draw_circle
        if value:
            self.draw_circle = value

    def within_range(self, event):
        '''
            self.within_rage(self, event) checks if the click event
            (event) passed in has a position within the range of the
            square where X or O is drawn. We check for the position
            on the event based on the drawing area given by
            self.drawing_area but we adjust for the margin between
            the drawing area and where the border is drawn.
            within_range: TicTacToeButton pygame.event.EventType -> (Anyof Bool None)
        '''
        position = event.pos
        left_boundary = self.drawing_area['left'] - self.margin
        right_boundary = self.drawing_area['right'] + self.margin
        up_boundary = self.drawing_area['top'] - self.margin
        down_boundary = self.drawing_area['bottom'] + self.margin
        if (left_boundary <= position[0]) and (right_boundary >= position[0]):
            if ((up_boundary <= position[1]) and \
                (down_boundary >= position[1])):
                return True

    def draw_piece(self, screen, event=None):
        '''
            self.click_handler(event, screen) handles a click event, comparing
            the (x,y) coordinates of the button with the (x, y) coordinates
            contained within the region where the figure will be drawn. If the
            figure has not been drawn, then set the self.start_time property
            to be the number of milliseconds that have since passed since
            pygame.init() was called. Until self.start_time is not none, the
            figure will not be drawn in the square, and this is only
            set when self.figure_drawn is False. self.figure_drawn will be
            False only once during the game. Essentially, this ensures that
            the animation for drawing the figure is done only once in a game.
            click_handler: TicTacToeButton pygame.event.EventType pygame.Surface -> None
        '''
        if not event:
            if not self.figure_drawn:
                self.start_time = pygame.time.get_ticks()
                self.figure_drawn = True
                return None
        if self.within_range(event):
            if not self.figure_drawn:
                self.start_time = pygame.time.get_ticks()
                self.figure_drawn = True

    def draw_boundary(self, screen):
        '''
            self.draw_boundary(screen) draws the boundary that makes up
            the board.
        '''
        top_left_y = self.drawing_area['top'] - self.margin - self.line_width
        top_left_x = self.drawing_area['left'] - self.margin - self.line_width
        width = self.drawing_area['right'] - self.drawing_area['left'] + \
                (2 * (self.margin + self.line_width))
        height = self.drawing_area['bottom'] - self.drawing_area['top'] + \
                (2 * (self.margin + self.line_width))
        pygame.draw.rect(screen, self.color, [top_left_y, top_left_x, width, height], self.line_width)

    def draw_line(self, starting_time, surface, start_pos, end_pos):
        '''
            self.draw_line(starting_time, surface, start_pos, end_pos)
        '''
        current_time = pygame.time.get_ticks()
        elapsed_time = float(current_time - starting_time)
        distance_x = end_pos[0] - start_pos[0]
        distance_y = end_pos[1] - start_pos[1]
        portion_drawn = min((elapsed_time / float(self.drawing_seconds)), 1)
        current_end_x = start_pos[0] + (distance_x * portion_drawn)
        current_end_y = start_pos[1] + (distance_y * portion_drawn)
        current_end = (current_end_x, current_end_y)
        pygame.draw.line(surface, self.color, start_pos, current_end, width = self.line_width)

    def draw_cross(self, surface):
        current_time = pygame.time.get_ticks()
        elapsed_time = float(current_time - self.start_time)
        line_drawing_time = float(self.drawing_seconds / 2)
        self.draw_line(self.start_time, surface, (self.drawing_area['left'], self.drawing_area['top']), \
                       (self.drawing_area['right'], self.drawing_area['bottom']))
        if (elapsed_time > line_drawing_time):
            second_start_time = self.start_time + line_drawing_time
            self.draw_line(second_start_time, surface, (self.drawing_area['right'], self.drawing_area['top']), \
                           (self.drawing_area['left'], self.drawing_area['bottom']))

    def draw_arc(self, surface):
        current_time = pygame.time.get_ticks()
        elapsed_time = float(current_time - self.start_time)
        portion_drawn = min((elapsed_time / float(self.drawing_seconds)), 1)
        start = 0.0
        end = math.pi * portion_drawn * 2
        width = self.drawing_area['right'] - self.drawing_area['left']
        height = self.drawing_area['bottom'] - self.drawing_area['top']
        rect = [self.drawing_area['left'], self.drawing_area['top'], width, height]
        pygame.draw.arc(surface, self.color, rect, start, end, width = self.line_width)

    def draw_shape(self, surface):
        if not self.start_time:
            return None
        if self.draw_circle:
            self.draw_arc(surface)
        else:
            self.draw_cross(surface)


if __name__ == '__main__':
    start_time = None
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    tic_tac_toe_button = TicTacToeButton(10, 15, 500, white, (250, 250), 200)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tic_tac_toe_button.click_handler(event, screen)
        screen.fill(black)
        start_time = tic_tac_toe_button.start_time
        tic_tac_toe_button.draw_boundary(screen)
        tic_tac_toe_button.draw_shape(screen)
        pygame.display.flip()
        timer.tick(60)
