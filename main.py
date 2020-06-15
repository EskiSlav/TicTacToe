import pygame

pygame.init()

FPS = 60

WHITE = (255,255,255)
BLACK = (0,  0,  0)
GREY = GRAY = (128,128,128)

WIDTH, HEIGHT = 450, 450
ROWS, COLS = 3, 3
[
  [ rect, rect, rect ],
  [ rect, rect, rect ],
  [ rect, rect, rect ]
]
wnd = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tik-Tak-Toe")

cross = pygame.image.load("Bullets/X_2D_Orange.png")
circle = pygame.image.load("Bullets/Disc_2D_Red.png")

def get_size(image: pygame.Surface, width: int):
	image_size = image.get_rect().size # get something like this: (400,200)
	return (width, int(image_size[1] * width / image_size[0]))

def resize_image(image: pygame.Surface, width):
	image_size = get_size(image, width)
	return pygame.transform.scale(image, image_size)

cross = resize_image(cross, int(WIDTH / ROWS))
circle = resize_image(circle, int(WIDTH / ROWS))

class Label:
    def __init__(self, text, x, y, font_size=30):
        self.font = pygame.font.Font("fonts/Sen-Bold.ttf", font_size) 
        self.text = text
        self.text_surf = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (x, y)

        self.back_rect = pygame.Rect(0, 0, self.text_rect.width + 50, self.text_rect.height + 20)
        self.back_rect.center = (x, y)
    
    def draw(self):
        pygame.draw.rect(wnd, GRAY, self.back_rect)
        wnd.blit(self.text_surf, self.text_rect)

class Button:
    font = pygame.font.Font("fonts/Sen-Bold.ttf", 28) 
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.back_rect = pygame.Rect(x, y, width, height)
        self.text_surf = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.back_rect.center

    def draw(self):
        pygame.draw.rect(wnd, GRAY, self.back_rect)
        wnd.blit(self.text_surf, self.text_rect)

    def collidepoint(self, x, y):
        if self.back_rect.collidepoint(x, y):
            return True
        return False

class ExitButton(Button):
    def __init__(self, text):
        x, y, button_width, button_height = WIDTH/2, HEIGHT/2 - 20, WIDTH/4, 40
        super().__init__(text, x, y, button_width, button_height)

    def action(self):
        exit()

class ResetButton(Button):
    def __init__(self, text):
        x = WIDTH/4
        y = HEIGHT/2 - 20
        button_width = WIDTH/4
        button_height =  40
        super().__init__(text, x, y, button_width, button_height)

    def action(self):
        return 1

class Playground():
    def __init__(self, playground_width = WIDTH, playground_height = HEIGHT):
        self.width  = playground_width
        self.height = playground_height
        

        # 1 - time to draw cross (tick)
        # 2 - time to draw circle 
        # cross moves first 
        self.turn   = 1 # cross (tick)

        self.rects  = []
        self.states = []
        self.create_playground()

    def create_playground(self, rows=3, cols=3):
        width  = self.width / rows 
        height = self.height / cols

        for y in ( j * height for j in range(cols) ):
            self.rects.append( [ pygame.Rect(x, y, width, height) for x in (x * width for x in range(rows)) ] )
            self.states.append([ 0 for _ in range(rows) ])

    def clear_playground(self, n=3, m=3):
        self.rects  = []
        self.states = []
        self.create_playground()


    def place(self, x, y):
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
        for rects_row, states_row in zip(self.rects, self.states):
            for rect, state in zip(rects_row, states_row):
                if state == 1:
                    wnd.blit(cross, rect)
                elif state == 2:
                    wnd.blit(circle, rect)

        width  = self.width / rows 
        height = self.height / cols

        for row in range(rows):
            pygame.draw.line(wnd, GRAY, (0, row * width), (WIDTH, row * width))

        for col in range(cols):
            pygame.draw.line(wnd, GRAY, (col * height, 0), (col * height, HEIGHT))

    def check_win(self):
        """ Dummy way but it works"""
        if self.check_draw():
            print("Draw")
            return self.check_draw()
        elif self.check_figure(1):
            print("Cross has won!")
            return self.check_figure(1)
        elif self.check_figure(2):
            print("Circle has won!")
            return self.check_figure(2)
        
        return False

    def check_draw(self):
        for row in self.states:
            for state in row:
                if not state:
                    return 0 
        else: 
            return -1

    def check_figure(self, figure):
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

    ExB = ExitButton("Exit")
    ReB = ResetButton("Reset")
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
        ExB.draw()
        ReB.draw()
        Caption.draw()


        pygame.display.update()


def game_loop():

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
            game_menu("X Won!")
            pg.clear_playground()
        if pg.check_win() == 2:
            game_menu("O Won!")
            pg.clear_playground()
        if pg.check_win() == -1:
            game_menu("Draw!")
            pg.clear_playground()
        pygame.display.update()

game_loop()
