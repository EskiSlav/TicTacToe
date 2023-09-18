from __future__ import annotations

import logging
from logging.config import dictConfig

import pygame
FORMAT = '[%(levelname)s] %(asctime)s %(name)s %(funcName)s: %(message)s'
LOGGING_LEVEL = logging.WARNING

logging_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
        },
    },
    'disable_existing_loggers': False,
}

dictConfig(logging_config)

logger = logging.getLogger(__name__)

pygame.init()

FPS = 3

WHITE = (255, 255, 255)
BLACK = (0,  0,  0)
GREY = GRAY = (128, 128, 128)

WIDTH, HEIGHT = 450, 450
ROWS, COLS = 3, 3

wnd = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

# images used (circle, cross)
cross = pygame.image.load('Bullets/X_2D_Orange.png')
circle = pygame.image.load('Bullets/Disc_2D_Red.png')


def get_size(image: pygame.Surface, width: int):
    image_size = image.get_rect().size  # get something like this: (400,200)
    return (width, int(image_size[1] * width / image_size[0]))


def resize_image(image: pygame.Surface, width):
    image_size = get_size(image, width)
    return pygame.transform.scale(image, image_size)


cross = resize_image(cross, int(WIDTH / ROWS))
circle = resize_image(circle, int(WIDTH / ROWS))


class Label:
    def __init__(self, text, x, y, font_size=30):
        logger.info('')
        self.font = pygame.font.Font(
            'fonts/Sen-Bold.ttf', font_size,
        )  # load font
        self.text = text  # save text
        self.text_surf = self.font.render(text, True, BLACK)  # render text
        # get rect from text to change its position
        self.text_rect = self.text_surf.get_rect()
        # changing text position to (x, y)
        self.text_rect.center = (x, y)

        # creating GRAY background and change its position to (x, y)
        self.back_rect = pygame.Rect(
            0, 0, self.text_rect.width + 50, self.text_rect.height + 20,
        )
        self.back_rect.center = (x, y)

    def draw(self):
        # logger.info('')
        pygame.draw.rect(wnd, GRAY, self.back_rect)
        wnd.blit(self.text_surf, self.text_rect)


class Button:
    font = pygame.font.Font('fonts/Sen-Bold.ttf', 28)

    def __init__(self, text, x, y, width, height):
        logger.info('')
        self.text = text
        self.back_rect = pygame.Rect(x, y, width, height)
        self.text_surf = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.back_rect.center

    def draw(self):
        # logger.info('')
        pygame.draw.rect(wnd, GRAY, self.back_rect)
        wnd.blit(self.text_surf, self.text_rect)

    def collidepoint(self, x, y):
        logger.info('')
        """ Checks if button is pressed """
        if self.back_rect.collidepoint(x, y):
            return True
        return False


class ExitButton(Button):
    def __init__(self, text):
        logger.info('')
        x, y, button_width, button_height = WIDTH/2, HEIGHT/2 - 20, WIDTH/4, 40
        super().__init__(text, x, y, button_width, button_height)

    def action(self):
        exit()


class ResetButton(Button):
    def __init__(self, text):
        logger.info('')
        x = WIDTH/4
        y = HEIGHT/2 - 20
        button_width = WIDTH/4
        button_height = 40
        super().__init__(text, x, y, button_width, button_height)

    def action(self):
        return 1


class Playground():
    def __init__(self, playground_width=WIDTH, playground_height=HEIGHT):
        logger.info('')
        self.width = playground_width
        self.height = playground_height

        # 1 - time to draw cross (tick)
        # 2 - time to draw circle
        # cross moves first
        self.turn = 1  # cross (tick)

        self.rects = []
        self.states = []  # state that shows is there placed rect, circle or nothing
        self.create_playground()

    def create_playground(self, rows=3, cols=3):
        logger.info('Creating playground')

        width = self.width / rows
        height = self.height / cols

        for y in (j * height for j in range(cols)):
            self.rects.append([
                pygame.Rect(x, y, width, height)
                for x in (x * width for x in range(rows))
            ])
            self.states.append([0 for _ in range(rows)])

    def clear_playground(self, n=3, m=3):
        """ Clears Playground after the end of the game """
        logger.info('')
        self.turn = 1
        self.rects = []
        self.states = []
        self.create_playground()

    def place(self, x, y):
        logger.info('')
        for i, row in enumerate(self.rects):
            for j, rect in enumerate(row):
                if rect.collidepoint(x, y):
                    if not self.states[i][j]:
                        self.states[i][j] = self.turn
                        if self.turn == 1:
                            self.turn = 2
                        else:
                            self.turn = 1
                    return

    def draw(self, rows=3, cols=3):
        """ Draws all lines, circles and crosses """
        # logger.info('')
        # Checking all rect and drawing circle or cross
        # based on what value is stored in self.states[i][j]
        for rects_row, states_row in zip(self.rects, self.states):
            for rect, state in zip(rects_row, states_row):
                if state == 1:
                    wnd.blit(cross, rect)
                elif state == 2:
                    wnd.blit(circle, rect)

        width = self.width / rows  # width  of single rect
        height = self.height / cols  # height of single rect

        # Drawing lines
        for row in range(rows):
            logger.info('Drawing row lines')
            pygame.draw.line(wnd, GRAY, (0, row * width), (WIDTH, row * width))

        for col in range(cols):
            logger.info('Drawing col lines')
            pygame.draw.line(
                wnd, GRAY, (col * height, 0),
                (col * height, HEIGHT),
            )

    def check_win(self):
        """ Dummy way but it works"""
        # logger.info('')
        if self.check_figure(1):
            print('Cross has won!')
            return self.check_figure(1)
        elif self.check_figure(2):
            print('Circle has won!')
            return self.check_figure(2)
        elif self.check_draw():
            print('Draw')
            return self.check_draw()

        return False

    def check_draw(self):
        """ Checking whether all rects are filled """
        # logger.info('')
        for row in self.states:
            for state in row:
                if not state:
                    return 0
        else:
            return -1

    def check_figure(self, figure):
        """ Checking if there is winning combination for cross or circle """
        # logger.info('')
        if (self.states[0][0] == figure and self.states[0][1] == figure and self.states[0][2] == figure) or \
           (self.states[1][0] == figure and self.states[1][1] == figure and self.states[1][2] == figure) or \
           (self.states[2][0] == figure and self.states[2][1] == figure and self.states[2][2] == figure) or \
           (self.states[0][0] == figure and self.states[1][0] == figure and self.states[2][0] == figure) or \
           (self.states[0][1] == figure and self.states[1][1] == figure and self.states[2][1] == figure) or \
           (self.states[0][2] == figure and self.states[1][2] == figure and self.states[2][2] == figure) or \
           (self.states[0][0] == figure and self.states[1][1] == figure and self.states[2][2] == figure) or \
           (self.states[2][0] == figure and self.states[1][1] == figure and self.states[0][2] == figure):
            return figure
        return 0


clock = pygame.time.Clock()


def game_menu(display_text: str):
    logger.info('')
    ExB = ExitButton('Exit')
    ReB = ResetButton('Reset')
    Caption = Label(display_text, int(WIDTH/2), int(HEIGHT/4), 50)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in (ExB, ReB):
                        if button.collidepoint(*event.pos):
                            if button.action():
                                return

        # Draw all the things
        ExB.draw()
        ReB.draw()
        Caption.draw()

        pygame.display.update()
        logger.info('updated')


def game_loop():
    logger.info('Entered game loop')
    pg = Playground()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pg.place(*event.pos)

        wnd.fill(WHITE)
        pg.draw()

        if pg.check_win() == 1:
            game_menu('X Won!')
            pg.clear_playground()
        if pg.check_win() == 2:
            game_menu('O Won!')
            pg.clear_playground()
        if pg.check_win() == -1:
            game_menu('Draw!')
            pg.clear_playground()

        pygame.display.update()


game_loop()
