import pygame

white = (0, 0, 0)

class Button:
    '''
        This class represents the creation of buttons on the screen.
        When clicking on these buttons, they will lead to a different
        page. The __init__ constructor takes 5 parameters:
        - coordinates: a tuple representing the (x, y) coordinates of
        the top left of the rectangular area for which the button will be
        inside. x and y are both 0 at the top left, and x increases as you
        go further right, while y increases as you go further down. In
        this rectangular area, the button will be centered horizontally
        and vertically. The x-coordinate of the top left of the button
        will be the width of the screen minus the first coordinate of the
        tuple minus the width of the button divided by 2 plus the value
        of the first coordinate in the tuple. The y-coordinate
        of the top left of the button will be second coordinate of the
        tuple entered plus the margin passed in.
        The coordinate of how the button is drawn should look like this,
        where (X, Y) represents the coordinates passed in:
                        screen width
        |--------------------------------------------------------------|
        |                                                              |
        |    (X, Y)                                                    |
        |   +----------------------------------------------------------|
        |   |(((screen width - X) - button width) / 2)      |          |
        |   |--------|                                      |(margin)  |
        |   |        +----------------------------------------+        |
        |   |       A|            (button width)              |B       |
        |   |        |                                        |        |
        |   |        |                                        |        |
        |   A =( ((((screen width - X) - button width) / 2) + X), (Y + margin) )
        |   |        |                                        |        |
        - width: the width of the button
        - height: the height of the button
        - text: the text that the button will show, if any
        - color: the color with which to display the button. The color will
        be a tuple of 3 integers representing rgb format.
        - text_color: the color the text in the button will be
        - next_page: the name of the configuration file that represents
        the next page
        - margin: the margin you want in between the buttons
        __init__: Tuple Int Int Str Tuple Tuple Str (Any of Int None) -> Button
    '''
    def __init__(self, coordinates, width, height, text, color, \
                 text_color, next_page, margin=10):
        self.coordinates = coordinates
        self.width = width
        self.height = height
        self.text = text
        self.next_page = next_page
        self.color = color
        self.text_color = text_color
        self.margin = margin

    def draw_button(self, screen, text_size, font_file=None):
        '''
            self.draw_button(screen, text_size, font_file) draws the buttton
            onto the surface represented by screen based on the passed in
            text_size, and font specified by font_file. If the text size is
            bigger than the button size, then the button size will be adjusted.
            If font_file is not passed in, it will be None and the default
            font specified by the desktop will be used.
            draw_button: Button pygame.Surface Int (Any of Str None) -> None
        '''
        text = pygame.font.Font(font_file, text_size)
        text_surface = text.render(self.text, True, self.text_color, self.color)
        text_size = text.size(self.text)
        # adjust the width and height of the button based on the
        # size of he text, adding more text or less
        self.width = max((text_size[0] + (2 * self.margin)), self.width)
        self.height = max((text_size[1] + (2 * self.margin)), self.height)
        y_coordinate = self.coordinates[1] + self.margin
        x_coordinate = int(((screen.get_width() - self.coordinates[0]) - self.width) / 2) + self.coordinates[0]
        first_button = pygame.draw.rect(
            screen, self.color,
            (x_coordinate, y_coordinate, self.width, self.height),
            0, int((min( self.width, self.height)) / 8)
        )
        text_x_coord = ((self.width - text_size[0]) / 2) + x_coordinate
        text_y_coord = ((self.height - text_size[1]) / 2) + y_coordinate
        screen.blit(text_surface, (text_x_coord, text_y_coord))

    def area(self, text_size, screen, font_file=None):
        '''
            self.area(text_size, screen, font_file) returns the area of
            the button based on the text size, the font specified by
            font_file, the starting coordinates of the button, the width
            of the button and the height of the button.
            area: Button Int pygame.Surface (Any of Str None) -> (List Tuple Tuple)
        '''
        text = pygame.font.Font(font_file, text_size)
        text_size = text.size(self.text)
        # adjust the width and height of the button based on the
        # size of he text, adding more text or less
        start_x = int(((screen.get_width() - self.coordinates[0]) - self.width) / 2) + self.coordinates[0]
        start_y = self.coordinates[1] + self.margin
        button_width = max((text_size[0] + (2 * self.margin)), self.width)
        button_height = max((text_size[1] + (2 * self.margin)), self.height)
        return [(start_x, start_y), ((start_x + button_width), (start_y + button_height))]

    def event_within_range(self, event, text_size, screen, font_file=None):
        '''
            self.event_within_range(event) takes a pygame.MOUSEBUTTONDOWN
            event and checks if the position of the event is within the
            range that the button is drawn on the screen.
            event_within_range: Button pygame.Event.EventType Int pygame.Surface (Any of Str None) -> Bool
        '''
        area = self.area(text_size, screen, font_file=None)
        position = event.pos
        if ((area[0][0] <= position[0]) and (position[0] <= area[1][0])):
            if ((area[0][1] <= position[1]) and (position[1] <= area[1][1])):
                return True
        return False
