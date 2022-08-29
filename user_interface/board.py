import pygame
import sys
import math
from cross_button import TicTacToeButton
from button import Button


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

class Board:
    '''
        This class represents the Board that will be used to draw the Tic Tac Toe pieces.
        The board takes in the following parameters:
        line_width - the line width used to determine the width of the boundary where the
        board is drawn
        margin - the margin in pixels between the drawing range and the border around a
        square on the board
        drawing_seconds - the number of milliseconds taken to draw a piece on the board
        color - a tuple or 3 integers between 0 and 255 representing the rgb color code
        of the color that will be used to draw the board and the pieces within the board.
        start - a tuple of 2 integers that represents the starting point of where to draw
        the board. This represents the top-left corner of where the board will be drawn,
        starting from the line itself.
        edge_length - the length of the edges that make up the square where the piece will
        be drawn.
    '''
    def __init__(self, line_width, margin, drawing_seconds, color, start, edge_length):
        self.board_pieces = [[], [], []]
        self.draw_circle = False
        self.drawing_start_time = None
        self.drawing_seconds = drawing_seconds
        self.line_width = line_width
        self.margin = margin
        self.color = color
        self.start = start
        self.edge_length = edge_length
        self.available_to_draw = True
        self.populate_the_board(line_width, margin, drawing_seconds, color, start, edge_length)

    def populate_the_board(self, line_width, margin, drawing_seconds, color, start, edge_length):
        '''
            self.populate_the_board(line_width, margin, drawing_seconds, color, start, edge_length)
            instantiates all pieces on the board, with the parameters passed in being the ones
            passed into the constructors for all the button objects used for the game. The coordinates
            for a specific piece on the board will be calculated by using the tuple passed in for the
            start, followed by the line width of the boundary and the margin of the different pieces
            on the board. line_width refers to the width of the border when drawing the game, and margin
            refers to the margin between the drawing area for the X or the O and the border. drawing_seconds
            refers to the number of seconds that will be taken to draw the piece on the board, and color
            refers to the color in which the pieces and the board will be drawn. start refers to the
            tuple that will be used to determine the top-left corner of the tic-tac-toe board. edge_length
            refers to the length of the edges of the square that makes up the drawing area.
            populate_the_board: Board Int Int Int Tuple Tuple Int -> None
        '''
        for index in range(3):
            y_coordinate = start[1] + line_width + margin + (index * ((line_width + (2 * margin)) + edge_length))
            for k in range(3):
                x_coordinate = start[0] + line_width + margin + (k * ((line_width + (2 * margin)) + edge_length))
                self.board_pieces[index].append(
                    TicTacToeButton(line_width, margin, drawing_seconds, color, (x_coordinate, y_coordinate), edge_length)
                )

    def draw_board(self, screen):
        '''
            self.draw_board(screen) draws the board on the screen and the
            individual board pieces onto the appropriate squares of the
            screen.
            draw_board: Board pygame.Surface -> None
        '''
        for row in self.board_pieces:
            for piece in row:
                piece.draw_boundary(screen)
                piece.draw_shape(screen)

    def switch_figures(self):
        '''
            self.switch_figures() switches the figure that is to be drawn
            on sections of the board where the piece isn't drawn. We do this
            because when you draw an X, the next piece should be an O.
            switch_figures: Board -> None
        '''
        for row in self.board_pieces:
            for piece in row:
                if not piece.figure_drawn:
                    piece.switch_figure()

    def clear_board(self):
        '''
            self.clear_board() clears the board by setting all the necessary
            properties in each piece on the board to its default value. Setting
            figure_drawn for a piece says that no pieces have been drawn there,
            and setting start_time to be None will stop the TicTacToeButton class
            from drawing on that section of the board. Setting the draw_circle
            property to be False will tell the TicTacToeButton class that
            an X should be drawn next. self.drawing_starting_time in conjunction
            with the current elapsed time since pygame.init() was called to
            determine if a piece is being drawn. By default,
            self.drawing_starting_time is set to None.
            clear_board: Board -> None
        '''
        for row in self.board_pieces:
            for piece in row:
                piece.start_time = None
                piece.figure_drawn = False
                piece.draw_circle = False
                self.drawing_start_time = None
    
    def click_handler(self, event, screen):
        '''
            self.click_handler(event, screen) this is the click handler
            function that handles click events. We first check if 
            the event is in range of where the button lies. If it is,
            check if self.drawing_start_time is set. If it is, then
            get the current time and check if enough time has elapsed
            for us to draw a new piece on the board. Check if
            the board is available for drawing (as sometimes it still may not
            be), and if it is then call the appropriate function
            to draw the piece on that area of the board. Adjust
            self.drawing_start_time accordingly, and switch
            what piece should be drawn on th board using
            self.switch_figures().
            click_handler: Board pygame.event.EventType pygame.Surface -> None
        '''
        for row in self.board_pieces:
            for piece in row:
                in_range = piece.within_range(event)
                if in_range:
                    if self.drawing_start_time:
                        current_time = pygame.time.get_ticks()
                        elapsed_time = current_time - self.drawing_start_time
                        not_busy = (elapsed_time >= self.drawing_seconds)
                        if not_busy and self.available_to_draw:
                            self.switch_figures()
                            self.drawing_start_time = pygame.time.get_ticks()
                            piece.draw_piece(screen, event)
                            return
                    else:
                        if self.available_to_draw:
                            self.switch_figures()
                            self.drawing_start_time = pygame.time.get_ticks()
                            piece.draw_piece(screen, event)
                            return

    def draw_manually(self, screen, coordinates):
        '''
            self.draw_manually(screen, coordinates) manually draw a piece on
            a section of the board. This is used when the minimax algorithm
            chooses where to put the next piece.
            draw_manually: Board pygame.Surface (List of Int Int) -> None
        '''
        self.board_pieces[coordinates[0]][coordinates[1]].draw_piece(screen)


if __name__ == '__main__':
    start_time = None
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    tic_tac_toe_board = Board(10, 15, 500, white, (105, 105), 120)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                tic_tac_toe_board.click_handler(event, screen)
        screen.fill(black)
        tic_tac_toe_board.draw_board(screen)
        pygame.display.flip()
        timer.tick(60)
