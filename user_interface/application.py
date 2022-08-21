import sys
import configparser
import pygame
from game_text import Text
from button import Button

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
width = 700
height = 700
FPS = 60
font_file = None



def load_text(config_vars):
    '''
        load_text(config_vars) given a configparser.ConfigParser object,
        return a list of all the loaded Text objects where the text lines
        are derived from the config file. The first item in the list is the
        header.
        load_text: ConfigParser -> (List of Text)
    '''
    font_file = config_vars['text_settings']['font_file']
    width = int(config_vars['game_settings']['width'])
    height = int(config_vars['game_settings']['height'])
    milliseconds_per_char = int(config_vars['text_settings']['milliseconds_per_char'])
    text_heading_size = int(config_vars['text_settings']['heading_size'])
    text_body_font_size = int(config_vars['text_settings']['body_size'])
    text_lines = []
    text_heading = config_vars['text']['heading']
    config_variables = {}
    for item in config_vars.items('text'):
        config_variables[item[0]] = item[1]
    counter = 1
    var_name = 'text_{0}'.format(counter)
    text_size = pygame.font.Font(font_file, text_heading_size).size(text_heading + '|')
    text_lines.append(
        Text(
            text_heading, text_heading_size, (0, 30), \
            (width, text_size[1] + 30), font_file, True, \
            milliseconds_per_char
        )
    )
    y_value = text_size[1] + 10
    body_text_size = pygame.font.Font(font_file, text_body_font_size).size("Sample text." + "|")
    line_height = body_text_size[1] + 20
    value = config_variables.get(var_name)
    while value:
        text_line = config_variables.get(var_name)
        y_value += line_height
        text_lines.append(
            Text(
                text_line, text_body_font_size, (0, y_value), \
                (width, (y_value + line_height)), font_file, True, \
                milliseconds_per_char
            )
        )
        counter += 1
        var_name = 'text_{0}'.format(counter)
        value = config_variables.get(var_name)
    return text_lines

def initialize_start_times(text_items):
    '''
        initialize_start_times(text_items) initializes the start animation times
        of the text items. The function assumes that the order of the items in
        text_items is he order in which they will be printed.
        initialize_start_times: (List of Text) -> None
    '''
    start_time = pygame.time.get_ticks()
    text_items[0].set_last_time(start_time)
    time_per_letter = text_items[0].seconds_per_letter
    word_animation_count = len(text_items[0].text) + 2
    delay = 400
    for index in range(1, len(text_items)):
        start_time += (time_per_letter * word_animation_count) + delay
        text_items[index].set_last_time(start_time)
        time_per_letter = text_items[index].seconds_per_letter
        word_animation_count = len(text_items[index].text) + 2
        delay += 75

def load_buttons(config):
    '''
        load_buttons(config) instantiates Button objects based on
        the settings in the configuration object. The parameters
        passed to the Button constructor are based on the values
        in the config object. The config object is a ConfigParser
        object from the built-in standard library configparser.
        Please see button.py for more information on the Button
        class. Each button has a section in the configuration file:
        button_1, button_2, etc. This is how specific settings to
        a button are stored in a standard format.
        load_buttons: ConfigParser -> (List of Button)
    '''
    width = int(config['buttons']['width'])
    height = int(config['buttons']['height'])
    button_text_size = int(config['buttons']['text_size'])
    text_color = pygame.Color(config['buttons']['text_color'])
    color = pygame.Color(config['buttons']['background'])
    text_color = (text_color.r, text_color.g, text_color.b)
    color = (color.r, color.g, color.b)
    x_start = int(config['buttons']['x_start'])
    y_start = int(config['buttons']['y_start'])
    buttons = []
    counter = 1
    button_key = 'button_{0}'.format(counter)
    while button_key in config:
        button_text = config[button_key]['text']
        next_page = config[button_key]['next_page']
        buttons.append(
            Button(
                (x_start, y_start), width, height, \
                button_text, color, text_color, \
                next_page
            )
        )
        y_start += (height + (2 * buttons[(counter - 1)].margin))
        counter +=1
        button_key = 'button_{0}'.format(counter)
    return buttons

def load_settings(config_file):
    '''
        load_settings(config_file) loads the settings from a config file
        and returns them in a dictionary, returns an empty dictionary
        if config_file can't be read.
        load_settings: Str -> Dict
    '''
    settings = {}
    config = configparser.ConfigParser()
    config_file = config.read(config_file)
    if config_file:
        settings['config'] = config
        settings['font_file'] = config['text_settings']['font_file']
        settings['FPS'] = int(config['game_settings']['frames_per_second'])
        settings['width'] = int(config['game_settings']['width'])
        settings['height'] = int(config['game_settings']['height'])
        settings['milliseconds_per_char'] = int(config['text_settings']['milliseconds_per_char'])
        text_items = load_text(config)
        settings['text_items'] = text_items
        settings['buttons'] = []
        if 'buttons' in config:
            buttons = load_buttons(config)
            settings['buttons'] = buttons
            settings['button_text_size'] = int(config['buttons']['text_size'])
    return settings

def click_handler(event, settings, screen):
    '''
    click_handler(event, settings, screen) the function to handle click
    events. The position of the click event is compared with the position
    of the all of buttons in settings['buttons'], and accordingly, the
    new page corresponding to that button is loaded in new_settings.
    new_settings is returned.
    click_handler: (List of pygame.event.EventType) Dict pygame.Surface -> Dict
    '''
    new_settings = {}
    for button in settings['buttons']:
        intersection = button.event_within_range(
            event, settings['button_text_size'], screen
        )
        if intersection:
            new_settings = load_settings(button.next_page)
            if new_settings:
                initialize_start_times(new_settings['text_items'])
                return new_settings
            else:
                raise Exception(
                    'The button that has been clicked has a next_page '
                    'property with the value of a configuration file '
                    'that cannot be opened.\nPlease check for the configuration '
                    'file named ' + button.next_page + '.\n'
                )
    return new_settings

def run_game():
    '''
    run_game() the entry point for our GUI application. When running this,
    the application will start up.
    '''
    pygame.init()
    timer = pygame.time.Clock()
    text_heading = "Tic Tac Toe"
    body = "hello"
    settings = load_settings('page_1.ini')
    button_text_size = 20
    if settings:
        width = settings['width']
        height = settings['height']
        FPS = settings['FPS']
        if 'button_text_size' in settings:
            button_text_size = settings['button_text_size']
    screen = pygame.display.set_mode((width, height))
    initialize_start_times(settings['text_items'])
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_settings = click_handler(event, settings, screen)
                if new_settings:
                    settings = new_settings
        screen.fill(black)
        if settings:
            for item in settings['text_items']:
                item.type_text(screen)
            for button in settings['buttons']:
                button.draw_button(screen, button_text_size)
        pygame.display.flip()
        timer.tick(FPS)

if __name__ == '__main__':
    run_game()
