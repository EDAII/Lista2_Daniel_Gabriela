import sys
import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (169, 169, 169)
YELLOW = (222, 178, 0)
PINK = (225, 96, 253)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
ORANGE = (255, 99, 71)
GRAY = (119, 136, 153)
LIGHTORANGE = (255, 176, 56)
INTERMEDIARYORANGE = (255, 154, 0)
LIGHTBLUE = (60, 170, 255)
DARKBLUE = (0, 101, 178)
BEIGE = (178, 168, 152)

SCREEN_BACKGROUND_COLOR = BLACK

SCREEN_MENU = 200
WIDTH = 1002 + SCREEN_MENU
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT)

MARGIN = 2

QTT = 100
MIN_HEIGHT = 10
MAX_HEIGHT = 580
RECTANGLE_THICKNESS = 8

WAIT_SELECTION_SORT = 4
WAIT_INSERTION_SORT = 60
WAIT_BUBBLE_SORT = 4
WAIT_SHELL_SORT = 15

def text(background, message, color, size, coordinate_x, coordinate_y):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    background.blit(text, [coordinate_x, coordinate_y])


class Rectangle():
    def __init__(self, height, width, color, pos_x, pos_y):
        self.height = height
        self.width = width
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])

    # Quando for atualizar apenas um dos retangulos e ele nao tiver trocado de posicao
    def update_rectangle_in_screen_animation(self, color, background, wait):
        self.color = color
        self.render(background)
        pygame.display.update()
        pygame.time.wait(wait)


class Rectangles():
    def __init__(self):
        self.set_rectangles = []

    def append_rectangle(self, rectangle):
        self.set_rectangles.append(rectangle)

    def render(self, background):
        initial_pos_x = MARGIN
        for rectangle in self.set_rectangles:
            rectangle.pos_x = initial_pos_x
            rectangle.render(background)
            initial_pos_x += RECTANGLE_THICKNESS + MARGIN

    # Quando for atualizar todos os retangulos porque teve troca de posicao (quando troca de posicao tem que desenhar tudo na tela novamente)
    def update_set_rectangles_in_screen_animation(self, background, wait):
        background.fill(SCREEN_BACKGROUND_COLOR)
        self.render(background)
        pygame.display.update()
        pygame.time.wait(wait)


class Game():
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')
        
        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Sort O(n²)')
        self.rectangles = self.create_rectangles()

        self.stoped = True

    def create_rectangles(self):
        rectangles = Rectangles()
        initial_pos_x = MARGIN
        random_heights = random.sample(range(MIN_HEIGHT, MAX_HEIGHT), QTT)

        for height in random_heights:
            rectangles.append_rectangle(Rectangle(height, RECTANGLE_THICKNESS, WHITE, initial_pos_x, HEIGHT - height - MARGIN))
            initial_pos_x += RECTANGLE_THICKNESS + MARGIN

        return rectangles

    def render(self):
        self.background.fill(SCREEN_BACKGROUND_COLOR)
        self.rectangles.render(self.background)

        if self.stoped:
            text(self.background, "(s) Selection Sort", ORANGE, 25, 1042, 20)
            text(self.background, "(i) Insertion Sort", ORANGE, 25, 1042, 50)
            text(self.background, "(b) Bubble Sort", ORANGE, 25, 1042, 80)
            text(self.background, "(h) Shell Sort", ORANGE, 25, 1042, 110)
            text(self.background, "(r) Retry", ORANGE, 25, 1042, 140)

    def run(self):
        exit = False
        
        while not exit:
            if self.stoped:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit = True
                        if event.key == pygame.K_s:
                            print("chamou selection sort")
                            self.stoped = False
                            selection_sort(self.rectangles, self.background)
                            self.stoped = True
                        if event.key == pygame.K_i:
                            print("chamou insertion sort")
                            self.stoped = False
                            insertion_sort(self.rectangles, self.background)
                            self.stoped = True
                        if event.key == pygame.K_b:
                            print("chamou bubble sort")
                            self.stoped = False
                            bubble_sort(self.rectangles, self.background)
                            self.stoped = True
                        if event.key == pygame.K_h:
                            print("chamou shell sort")
                            self.stoped = False
                            shell_sort(self.rectangles, self.background)
                            self.stoped = True
                        if event.key == pygame.K_r:
                            main()
            
            self.render()
            pygame.display.update()

        pygame.quit()
        sys.exit(0)

# Selection Sort
def selection_sort(rectangles, background):
    for i in range(len(rectangles.set_rectangles)):
        min_index = i

        rectangles.set_rectangles[min_index].update_rectangle_in_screen_animation(RED, background, WAIT_SELECTION_SORT)

        for j in range(i + 1, len(rectangles.set_rectangles)):

            if j > 0 and rectangles.set_rectangles[j - 1].color == BLUE:
                rectangles.set_rectangles[j - 1].update_rectangle_in_screen_animation(WHITE, background, WAIT_SELECTION_SORT)
    
            rectangles.set_rectangles[j].update_rectangle_in_screen_animation(BLUE, background, WAIT_SELECTION_SORT)

            if rectangles.set_rectangles[j].height < rectangles.set_rectangles[min_index].height:

                rectangles.set_rectangles[min_index].update_rectangle_in_screen_animation(WHITE, background, WAIT_SELECTION_SORT)
                rectangles.set_rectangles[j].update_rectangle_in_screen_animation(RED, background, WAIT_SELECTION_SORT)

                min_index = j

        aux_rectangle = rectangles.set_rectangles[i]
        rectangles.set_rectangles[i] = rectangles.set_rectangles[min_index]
        rectangles.set_rectangles[min_index] = aux_rectangle

        if rectangles.set_rectangles[len(rectangles.set_rectangles) - 1].color == BLUE:
            rectangles.set_rectangles[len(rectangles.set_rectangles) - 1].color = WHITE

        rectangles.set_rectangles[i].color = GREEN
        
        rectangles.update_set_rectangles_in_screen_animation(background, WAIT_SELECTION_SORT)

# Insertion Sort
def insertion_sort(rectangles, background):

    # pinta o rectangles.set_rectangles[0] de verde e renderiza
    rectangles.set_rectangles[0].update_rectangle_in_screen_animation(GREEN, background, WAIT_INSERTION_SORT)
    for i in range(1, len(rectangles.set_rectangles)):
        j = i
        # pinta o rectangles.set_rectangles[j] de vermelho e renderiza
        rectangles.set_rectangles[j].update_rectangle_in_screen_animation(RED, background, WAIT_INSERTION_SORT)
        while ((j != 0) and rectangles.set_rectangles[j].height < rectangles.set_rectangles[j - 1].height):
            # troca ate chegar na posicao dele
            # ao trocar renderiza todos os rect novamente
            rectangles.set_rectangles[j - 1].color = GREEN

            aux = rectangles.set_rectangles[j]
            rectangles.set_rectangles[j] = rectangles.set_rectangles[j - 1]
            rectangles.set_rectangles[j - 1] = aux

            rectangles.update_set_rectangles_in_screen_animation(background, WAIT_INSERTION_SORT)
            j -= 1
        # pinta o rectangles.set_rectangles[j] de verde e renderiza
        rectangles.set_rectangles[j].update_rectangle_in_screen_animation(GREEN, background, WAIT_INSERTION_SORT)


# Bubble Sort
# a cada iteracao ele leva um maior para sua posicao final
def bubble_sort(rectangles, background):
    for i in range(len(rectangles.set_rectangles)):
        # i elementos ordenados ao final
        # pinta rectangles.set_rectangles[j] de vermelho e renderiza
        for j in range(len(rectangles.set_rectangles) - i - 1):
            rectangles.set_rectangles[j].update_rectangle_in_screen_animation(RED, background, WAIT_BUBBLE_SORT)
            if rectangles.set_rectangles[j].height > rectangles.set_rectangles[j + 1].height:
                aux = rectangles.set_rectangles[j]
                rectangles.set_rectangles[j] = rectangles.set_rectangles [j + 1]
                rectangles.set_rectangles[j + 1] = aux
                # mantem cores
                # faz a troca de posicao e renderiza tudo novamente
                rectangles.update_set_rectangles_in_screen_animation(background, WAIT_BUBBLE_SORT)
            else:
                rectangles.set_rectangles[j].update_rectangle_in_screen_animation(WHITE, background, WAIT_BUBBLE_SORT)
                rectangles.set_rectangles[j + 1].update_rectangle_in_screen_animation(RED, background, WAIT_BUBBLE_SORT)
                # pinta o novo maior de vermelho
                # pinta o antigo vermelho de branco
                # pinta rectangles.set_rectangles[j] de branco e renderiza
                # pinta rectangles.set_rectangles[j + 1] de vermelho e renderiza
        # pinta o ultimo de verde e renderiza
        rectangles.set_rectangles[len(rectangles.set_rectangles) - i - 1].update_rectangle_in_screen_animation(GREEN, background, WAIT_BUBBLE_SORT)

# Shell Sort
def shell_sort(rectangles, background):
    # determina gap inicial como tamanho do vetor dividido por 2
    last = False
    gap = len(rectangles.set_rectangles) // 2
    while gap > 0:
        if gap == 1:
            last = True
            
        # loop começando de gap ate o tamanho do vetor
        for i in range(gap, len(rectangles.set_rectangles)):
            temp = rectangles.set_rectangles[i]

            rectangles.set_rectangles[i].update_rectangle_in_screen_animation(RED, background, WAIT_SHELL_SORT)
            rectangles.set_rectangles[i - gap].update_rectangle_in_screen_animation(BLUE, background, WAIT_SHELL_SORT)

            j = i
            # comeca do gap e verifica se os elementos dentro do gap dele para tras estao ordenados
            while j >= gap and rectangles.set_rectangles[j - gap].height > temp.height:
                
                rectangles.set_rectangles[j - gap].update_rectangle_in_screen_animation(BLUE, background, WAIT_SHELL_SORT)

                rectangles.set_rectangles[j] = rectangles.set_rectangles[j - gap]
                j -= gap

            rectangles.set_rectangles[j] = temp

            if not last:
                rectangles.set_rectangles[j].color = WHITE
                rectangles.set_rectangles[i - gap].color = WHITE
                z = i
                while z >= gap:
                    rectangles.set_rectangles[z].color = WHITE
                    z -= gap
            else:
                rectangles.set_rectangles[j].color = GREEN
                rectangles.set_rectangles[i - gap].color = GREEN
                z = i
                while z >= gap:
                    rectangles.set_rectangles[z].color = GREEN
                    z -= gap

            rectangles.update_set_rectangles_in_screen_animation(background, WAIT_SHELL_SORT)


        # divide o gap por 2
        gap = gap // 2
        # na ultima iteracao do gap quando comparar o vermelho com o azul
        # os azuis se tornam verde por ja estarem ordenados

def main():
    mygame = Game()
    mygame.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interruption')