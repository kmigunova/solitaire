import pygame
import random
import os
import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
# from amount import Ui_Dialog

AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)  # РУБАШКА КАРТЫ
WHITE = (255, 255, 255)

pygame.init()

# выбор кол-ва карт при раздаче
# ДОДЕЛАТЬ !!!
'''class Dialog(QFileDialog, Ui_Dialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.card_1.clicked.connect(self.one)
        self.card_3.clicked.connect(self.three)
        self.choice.setChecked(True)'''
# здесь ещё можно сделать выбор типа доски: стандартная или лас-вегас
# в лас-вегасе колоду можно просматривать 2 или 3 раза
# а в стандарте - сколько угодно


FPS = 50
WIDTH = 775
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# bg_music = ['sting_-_windmills_of_your_mind.mp3', 'sting_-_shape_of_my_heart.mp3']

# for elem in bg_music:
pygame.mixer.music.load('sting_-_windmills_of_your_mind.mp3')
pygame.mixer.music.play(-1, 0.0)


def terminate():
    pygame.quit()
    sys.exit()


def load_background(name, colorkey=None):
    fullname = os.path.join('pics', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class GameOver(pygame.sprite.Sprite):
    image = load_background("over.jpg")

    def __init__(self, group):
        super().__init__(group)
        self.image = GameOver.image
        self.rect = self.image.get_rect()
        self.vx = 10
        self.rect.left -= 600

    def update(self):
        if self.rect.left + self.rect.width < width or self.rect.left > 0:
            self.image = GameOver.image
            self.rect.left += self.vx


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


# back = load_image('back.png')


def start_screen():
    fon = pygame.transform.scale(load_background('bg.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Moved_card(object):
    moved = False  # все карты стоят ровно на своих местах
    moved_card = []
    card_d = ()
    cards = None

    def click_up(self, deck_list):
        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, Deck_2):
                    if item.check_pos() and item.check_card(self.moved_card):
                        item.add_card(self.moved_card)
                        self.moved = False
                        self.moved_card = []
                        if isinstance(self.cards, Deck_1):
                            self.cards.show_card()
                        self.cards = None
                        break
            else:
                self.cards.add_card(self.moved_card)
                self.moved = False
                self.moved_card = []
                self.cards = None

    def draw(self, screen, card_dict):
        # передвижение карт на экране
        if self.moved:
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.card_d[0]
            y = pos[1] - self.card_d[1]
            for item in self.moved_card:
                screen.blit(card_dict[item], [x, y])
                y += 32  # чем эта переменная больше, тем сильнее
                # отдалаются друг от друга карты, когда тащишь несколько


class Deck(object):

    def __init__(self, x, y):
        self.cards = []
        self.rect = pygame.Rect(x, y, 71, 96)

    def check_pos(self):
        # если курсор наведёен на карту
        pos = pygame.mouse.get_pos()
        if pos[0] >= self.rect.left and pos[0] <= self.rect.right:
            if pos[1] >= self.rect.top and pos[1] <= self.rect.bottom:
                return True
            else:
                return False
        else:
            return False


class Deck_1(Deck):

    def __init__(self, x, y):
        Deck.__init__(self, x, y)
        self.y = y
        self.hidden = []

    def extend_list(self, lst):
        self.hidden.extend(lst)
        self.cards.append(self.hidden.pop())
        if len(self.hidden) > 0:
            for i in range(len(self.hidden)):
                self.rect.top += 32

    def draw_card(self, screen, card_dict):
        # числа - это границы ячеек
        # если их изменить, всё слипнется
        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 71, 96], 2)
        i = self.y
        if len(self.hidden) > 0:
            for item in self.hidden:
                pygame.draw.rect(screen, TEAL, [self.rect.left, i, 71, 96])
                pygame.draw.rect(screen, BLACK, [self.rect.left, i, 71, 96], 2)
                i += 32
        if len(self.cards) > 0:
            for item in self.cards:
                screen.blit(card_dict[item], [self.rect.left, i])
                i += 32

    def add_card(self, card):
        if len(self.cards) > 0 or len(self.hidden) > 0:
            for i in range(len(card)):
                self.rect.top += 32
        else:
            for i in range(len(card)):
                if i > 0:
                    self.rect.top += 32
        self.cards.extend(card)

    def click_down(self, card):
        # при нажатии на мышку
        if len(self.cards) > 0:
            top = self.rect.top
            lst = []
            for i in range(len(self.cards)):
                if self.check_pos():
                    pos = pygame.mouse.get_pos()
                    lst.insert(0, self.cards.pop())
                    card.card_d = (pos[0] - self.rect.left, pos[1] -
                                   self.rect.top)
                    card.moved = True
                    card.cards = self
                    card.moved_card.extend(lst)
                    if len(self.cards) > 0 or len(self.hidden) > 0:
                        self.rect.top -= 32
                    break
                else:
                    lst.insert(0, self.cards.pop())
                    self.rect.top -= 32
            else:
                self.rect.top = top
                self.cards.extend(lst)

    def show_card(self):
        if len(self.cards) == 0 and len(self.hidden) > 0:
            self.cards.append(self.hidden.pop())

    def check_card(self, moved_card):
        card = moved_card[0]
        result = False
        if len(self.cards) == 0:
            if "king" in card:
                result = True
        else:
            if "hearts" in card or "diamonds" in card:
                if "spades" in self.cards[-1] or "clubs" in self.cards[-1]:
                    next_card = "X"
                    if "king" in self.cards[-1]:
                        next_card = "queen"
                    elif "queen" in self.cards[-1]:
                        next_card = "jack"
                    elif "jack" in self.cards[-1]:
                        next_card = "10_"
                    elif "10_" in self.cards[-1]:
                        next_card = "9_"
                    elif "9_" in self.cards[-1]:
                        next_card = "8_"
                    elif "8_" in self.cards[-1]:
                        next_card = "7_"
                    elif "7_" in self.cards[-1]:
                        next_card = "6_"
                    elif "6_" in self.cards[-1]:
                        next_card = "5_"
                    elif "5_" in self.cards[-1]:
                        next_card = "4_"
                    elif "4_" in self.cards[-1]:
                        next_card = "3_"
                    elif "3_" in self.cards[-1]:
                        next_card = "2_"
                    elif "2_" in self.cards[-1]:
                        next_card = "ace"

                    if next_card in card:
                        result = True
            elif "hearts" in self.cards[-1] or "diamonds" in self.cards[-1]:
                next_card = "X"
                if "king" in self.cards[-1]:
                    next_card = "queen"
                elif "queen" in self.cards[-1]:
                    next_card = "jack"
                elif "jack" in self.cards[-1]:
                    next_card = "10_"
                elif "10_" in self.cards[-1]:
                    next_card = "9_"
                elif "9_" in self.cards[-1]:
                    next_card = "8_"
                elif "8_" in self.cards[-1]:
                    next_card = "7_"
                elif "7_" in self.cards[-1]:
                    next_card = "6_"
                elif "6_" in self.cards[-1]:
                    next_card = "5_"
                elif "5_" in self.cards[-1]:
                    next_card = "4_"
                elif "4_" in self.cards[-1]:
                    next_card = "3_"
                elif "3_" in self.cards[-1]:
                    next_card = "2_"
                elif "2_" in self.cards[-1]:
                    next_card = "ace"

                if next_card in card:
                    result = True

        return result


class Deck_2(Deck):
    def __init__(self, x, y):
        Deck.__init__(self, x, y)
        self.hidden_cards = []
        self.cards_list = []
        self.x = x

    def click_down(self, card):
        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            c = self.cards.pop()
            card.moved_card.append(c)
            self.cards_list.remove(c)
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self
            self.rect.left -= 20
        else:
            pos = pygame.mouse.get_pos()
            flag = False
            if pos[0] >= 30 and pos[0] <= 101:
                if pos[1] >= 30 and pos[1] <= 126:
                    flag = True
            if flag:
                self.rect.left = self.x
                if len(self.hidden_cards) > 0:
                    self.cards = []
                    for i in range(3):
                        c = self.hidden_cards.pop()
                        self.cards_list.insert(0, c)
                        self.cards.append(c)
                        if len(self.hidden_cards) == 0 and i < 2:
                            break

                else:
                    self.hidden_cards.extend(self.cards_list)
                    self.cards_list = []
                    self.cards = []

                if len(self.cards) > 1:
                    for i in range(len(self.cards)):
                        if i > 0:
                            self.rect.left += 20

    def draw_card(self, screen, card_dict):
        x = self.x
        if len(self.hidden_cards) > 0:
            pygame.draw.rect(screen, TEAL, [30, 30, 71, 96])
            pygame.draw.rect(screen, BLACK, [30, 30, 71, 96], 2)  # обводка колоды
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20  # расстояние между левыми верхними углами
                    # видимых карт в колоде
        else:
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20  # на сколько видны 3 последние карты в колоде
            pygame.draw.ellipse(screen, OLIVE, [40, 40, 60, 60], 5)
            # круг на внутренней стороне колоды

    def add_card(self, card):
        self.cards.extend(card)
        self.cards_list.extend(card)
        self.rect.left += 20


class Deck_3(Deck):
    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:3] == 'ace':
                    result = True
            else:
                suit = self.cards[0][4:]
                next_card = ''
                if suit in card:
                    if 'ace' in self.cards[-1]:
                        next_card = '2_' + suit
                    elif '2_' in self.cards[-1]:
                        next_card = '3_' + suit
                    elif '3_' in self.cards[-1]:
                        next_card = '4_' + suit
                    elif '4_' in self.cards[-1]:
                        next_card = '5_' + suit
                    elif '5_' in self.cards[-1]:
                        next_card = '6_' + suit
                    elif '6_' in self.cards[-1]:
                        next_card = '7_' + suit
                    elif '7_' in self.cards[-1]:
                        next_card = '8_' + suit
                    elif '8_' in self.cards[-1]:
                        next_card = '9_' + suit
                    elif '9_' in self.cards[-1]:
                        next_card = '10_' + suit
                    elif '10_' in self.cards[-1]:
                        next_card = 'jack_' + suit
                    elif 'jack_' in self.cards[-1]:
                        next_card = 'queen_' + suit
                    elif 'queen_' in self.cards[-1]:
                        next_card = 'king_' + suit

                    if next_card == card:
                        result = True
        return result

    def click_down(self, card):
        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            card.moved_card.append(self.cards.pop())
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
            card.moved = True
            card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    def draw_card(self, screen, card_dict):
        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 71, 96], 2)  # ДОМА !!!!!!
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])


def shuffle_cards():
    # перемешиваем карты
    r = []
    lst = ["ace_clubs", "2_clubs", "3_clubs", "4_clubs",
           "5_clubs", "6_clubs", "7_clubs", "8_clubs",
           "9_clubs", "10_clubs", "jack_clubs", "queen_clubs",
           "king_clubs", "ace_spades", "2_spades", "3_spades",
           "4_spades", "5_spades", "6_spades", "7_spades",
           "8_spades", "9_spades", "10_spades", "jack_spades",
           "queen_spades", "king_spades", "ace_hearts", "2_hearts",
           "3_hearts", "4_hearts", "5_hearts", "6_hearts",
           "7_hearts", "8_hearts", "9_hearts", "10_hearts",
           "jack_hearts", "queen_hearts", "king_hearts", "ace_diamonds",
           "2_diamonds", "3_diamonds", "4_diamonds", "5_diamonds",
           "6_diamonds", "7_diamonds", "8_diamonds", "9_diamonds",
           "10_diamonds", "jack_diamonds", "queen_diamonds", "king_diamonds"]

    length = len(lst)
    for i in range(length):
        if len(lst) > 1:
            c = random.choice(lst)
            r.append(c)
            lst.remove(c)
        else:
            c = lst.pop()
            r.append(c)

    return r


start_screen()
running = True


def main():
    done = False
    pygame.display.set_caption("Solitaire")
    suits = ["clubs", "spades", "hearts", "diamonds"]

    names = ["ace", "2", "3", "4", "5", "6",
             "7", "8", "9", "10", "jack", "queen",
             "king"]

    card_dict = {}

    for card in names:
        for suit in suits:
            img = pygame.image.load("data/" + card + "_" + suit + ".png").convert()
            card_dict[card + "_" + suit] = img

    card_list = shuffle_cards()
    # всё, что находится на экране
    deck_list = [Deck_2(130, 30), Deck_1(30, 160), Deck_1(130, 160), Deck_1(230, 160),
                 Deck_1(330, 160), Deck_1(430, 160), Deck_1(530, 160), Deck_1(630, 160),
                 Deck_3(330, 30), Deck_3(430, 30), Deck_3(530, 30), Deck_3(630, 30)]
    '''первое - координаты колоды;
    второе - координаты карт в ячейке под колодой;
    третье - координаты второй слева ячейки;
    четвёртое - координаты третьей слева ячейки;
    пятое - координаты четвёртой слева ячейуки;
    шестое - координаты пятой слева ячейки;
    седьмое - координаты шестой слева ячейки;
    восьмое - координаты седьмой слева ячейки;
    девятое - координаты первой ячейки дома:
    десятое - координаты второй ячейки дома:
    одиннадцатое - координаты третьей ячейки дома:
    двенадцатое - координаты четвёртой ячейки дома:
    '''
    m_card = Moved_card()
    deck_list[1].extend_list(card_list[:1])
    del card_list[:1]
    deck_list[2].extend_list(card_list[:2])
    del card_list[:2]
    deck_list[3].extend_list(card_list[:3])
    del card_list[:3]
    deck_list[4].extend_list(card_list[:4])
    del card_list[:4]
    deck_list[5].extend_list(card_list[:5])
    del card_list[:5]
    deck_list[6].extend_list(card_list[:6])
    del card_list[:6]
    deck_list[7].extend_list(card_list[:7])
    del card_list[:7]

    deck_list[0].hidden_cards.extend(card_list)
    game_over = False
    fnt = 'Georgia'
    text = pygame.font.SysFont(fnt, 30).render("Congratulations, "
                                               "You Won!", True, BLACK)
    # text = font.render("Congratulations, You Won!", True, BLACK)
    '''здесь будет сценарий на победу;
    после него - статистика'''
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in deck_list:
                    item.click_down(m_card)

            if event.type == pygame.MOUSEBUTTONUP:
                m_card.click_up(deck_list)


        for item in deck_list:
            if isinstance(item, Deck_3):
                if len(item.cards) != 13:
                    break
        else:
            game_over = True
            # screen.fill(OLIVE)
            # scenary_over = True
            if game_over:
                screen.fill(AQUA)
                screen.blit(text, [250, 250])
            '''сценарий на проигрыш
            работает или нет, пока не знаю'''
            '''while scenary_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        scenary_over = False
                # screen.fill(BLUE)
                # all_sprites.draw(screen)
                # all_sprites.update()
                pygame.display.flip()'''
        screen.fill((0, 100, 0))
        # статистика


        for item in deck_list:
            item.draw_card(screen, card_dict)
        m_card.draw(screen, card_dict)
        if game_over:
            pygame.draw.rect(screen, AQUA, [245, 246, 250, 25])
            screen.blit(text, [250, 250])
        pygame.display.flip()

        clock.tick(20)

    terminate()


if __name__ == '__main__':
    main()
