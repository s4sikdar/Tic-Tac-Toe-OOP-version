import pygame
import sys

class Text:
    '''
        Text class to represent text. The constructor takes:
        - text: the text to be represented
        - text_size: the font size in an integer
        - start: a tuple representing the starting x, y coordinates
            that the text should be in on the screen
        - end: a tuple representing the ending x, y coordinates that the
            text should be in on the screen
        - font_file: the name of the file representing the font of the text.
            By default, this will be None and the default font in the computer
            will be used.
        - animation: a Boolean that if set to True, means that the text
            will be animated. True is the default.
        - seconds_per_letter: the time taken to type each character when
            the typing animation goes underway.
        - color: the text color, which is white by default.
        - background: the background color of the text, which is black by default
        The parameters end combined with start should be a box on the
        screen for which text will go inside. The user of the class must
        first figure out the width and height of the text with the given
        font and the given font-size before initializing an instance of
        the class. The constructor will find the width and height of the
        surface require to store the text along with the character '|'.
        If the width or height exceeds the size of the rectangle provided
        by the box created from start and end, an exception will be raised.
        __init__: Str Int Tuple Tuple (Any of Str None) (Any of Bool None)
                 (Anyof Int None) (Anyof Tuple None) (Any of Tuple None)-> Text
    '''
    def __init__(self, text, text_size, start, end, font_file = None, \
                 animation=True, seconds_per_letter=400, color = (255, 255, 255), background = (0, 0, 0)):
        self.text = text
        self.seconds_per_letter = seconds_per_letter
        self.text_in_progress = '|'
        self.animation = animation
        self.start_time = None
        self.last_type = None
        self.length_so_far = 0
        self.start = start
        self.end = end
        self.text_font = pygame.font.Font(font_file, text_size)
        self.color = color
        self.background = background
        text_dimensions = self.text_font.size(text + '|')
        width = end[0] - start[0]
        height = end[1] - start[1]
        if (width < 0) or (height < 0):
            raise Exception((
                'The coordinates represented by the parameters start and end are invalid.\n'
                'The values in the tuple for the start parameter must be less than the values for '
                'the tuple for the end parameter.\n'
                'See the docstring for the Text class by running help(Text) for more information.\n'
            ))
        if (width < text_dimensions[0]) or (height < text_dimensions[1]):
            raise Exception((
                'The text will not be contained in the area represented by the parameters start and end.\n'
                'See the docstring for the Text class by running help(Text) for more information.\n'
                ))

    def set_last_time(self, time = None):
        '''
            self.set_last_time(time) sets the self.last_type attribute
            to the given time passed in. If no time is passed in, set
            self.last_type equal to the current number of milliseconds
            that have passed since pygame.init() was called using
            pygame.time.get_ticks().
            set_last_time: Text (Any of Int None) -> None
        '''
        if not time:
            self.last_type = pygame.time.get_ticks()
        else:
            self.last_type = time

    def text_animate(self, screen, coordinates):
        '''
            self.text_animate(coordinates) animates the typing of text
            onto the screen, with the tuple passed in for coordinates
            representing the coordinates of the top left corner of the
            text box. The screen is represented by the parameter passed
            in.
            text_animate: Text Surface Tuple -> None
        '''
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_type
        if ((elapsed_time // self.seconds_per_letter) >= 1):
            if ((self.length_so_far) == ((len(self.text)) + 1)):
                self.text_in_progress = self.text
            else:
                self.length_so_far += 1
                length = len(self.text)
                if (self.length_so_far > length):
                    self.text_in_progress = self.text
                else:
                    self.text_in_progress = self.text[:self.length_so_far] + '|'
            self.set_last_time()
        text_surface = self.text_font.render(
            self.text_in_progress, True, self.color, self.background
        )
        screen.blit(text_surface, coordinates)

    def type_text(self, screen, coordinates=None):
        '''
            type_text(self, coordinates) types text with the top corner
            being the coordinates to type the text. coordinates can be
            optionally entered to specify where in the text box to display
            the text. The default behaviour is that the text will be centered
            in the text box. So if when this class is instantiated, the text box
            specified by start and end goes from (0, 0) to (300, 200), and the
            space taken by the text is a rectangle of width 100 and height 50,
            the coordinates of the top left corner of where the text will be
            displayed are going to be (100, 75). The coordinates of the
            bottom right of where the full text is displayed will be
            (200, 125). If you wanted the top right corner of the text to be
            (150, 125) then the function would do this. The function will raise
            an exception of the text can't fit in the given box based on the
            coordinates provided. If you pass in coordinates, you must ensure the
            coordinates provide enough room for the text to be placed in the box.
            Requires: The tuple for coordinates must be of size 2.
            The screen parameter passed in represents the screen to draw in.
            type_text: Text Surface (Anyof Tuple None) -> None
        '''
        current_time = pygame.time.get_ticks()
        if self.last_type:
            if self.last_type > current_time:
                return None
        text_dimensions = self.text_font.size(self.text + '|')
        if coordinates:
            width = self.end[0] - coordinates[0]
            height = self.end[1] - coordinates[1]
            if (text_dimensions[0] > width) or (text_dimensions[1] > height):
                raise Exception((
                    'The coordinates provided do not provide enough room for the '
                    'text to be rendered in the text box calculated based on the '
                    'parameters passed in to the Text class\'s constructor.\n'
                    'See the docstring of the Text class and the docstring of '
                    'the Text.type_text method by typing help(Text) and help(Text.type_text) '
                    'respectively.\n'
                    ))
        else:
            text_dimensions = self.text_font.size(self.text)
            width = self.end[0] - self.start[0]
            height = self.end[1] - self.start[1]
            x_coord = ((width - text_dimensions[0]) / 2) + self.start[0]
            y_coord = ((height - text_dimensions[1]) / 2) + self.start[1]
            coordinates = (x_coord, y_coord)
        self.text_animate(screen, coordinates)
