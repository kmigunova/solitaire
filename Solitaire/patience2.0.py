import pygame
import random
import os
import sys
import pickle
from copy import deepcopy
import deck
from pygame.locals import *
import time


AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 130)
GRAY = (100, 100, 100)

pygame.init()


TEXT = ["Congratulations, You Won!", "New Game", "    Mute", "  Unmute"]
FPS = 100
SIZE = WIDTH, HEIGHT = 820, 670
TYPE = 1
KOL = 1
fnt = 'Times New Roman'

screen = pygame.display.set_mode(SIZE, HWSURFACE | DOUBLEBUF | RESIZABLE)
clock = pygame.time.Clock()

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


back = load_image('back.png')


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


def finish_screen():
    screen.fill(TEAL)
    screen.blit(pygame.font.SysFont(fnt, 35).render(TEXT[0], True, BLACK), [250, 250])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            else:
                main()
        pygame.display.flip()
        clock.tick(FPS)
    return


class Moved_card(object):

    def __init__(self):
        self.moved = False
        self.moved_card = list()
        self.card_d = ()
        self.cards = None

    def click_up(self, deck_list):
        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, Deck_2):
                    if item.check_pos() and item.check_card(self.moved_card):
                        item.add_card(self.moved_card)
                        self.moved = False
                        self.moved_card = list()
                        if isinstance(self.cards, Deck_1):
                            self.cards.show_card()
                        self.cards = None
                        break
            else:
                self.cards.add_card(self.moved_card)
                self.moved = False
                self.moved_card = list()
                self.cards = None

    def draw(self, screen, card_dict):
        if self.moved:
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.card_d[0]
            y = pos[1] - self.card_d[1]
            for item in self.moved_card:
                screen.blit(card_dict[item], [x, y])
                y += 32


class Deck(object):
    def __init__(self, x, y):
        self.cards = []
        self.rect = pygame.Rect(x, y, 71, 96)
        self.score = 0

    def check_pos(self):
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
        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 71, 96], 2)
        i = self.y
        if len(self.hidden) > 0:
            for item in self.hidden:
                screen.blit(back, [self.rect.left, i, 71, 96])
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

    def check_card(self,moved_card):
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
            screen.blit(back, (30, 30))
            pygame.draw.rect(screen, BLACK, [30, 30, 71, 99], 2)
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
        else:
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
            pygame.draw.ellipse(screen, OLIVE, [40, 40, 60, 60], 5)

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
        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 71, 96], 2)
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])


def shuffle_cards():
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


all_sprites = pygame.sprite.Group()


def main():
    global score, vremya, best_time, best_score, total_score, time_bonus, played, won, pers

    file_read = open('statistics.txt', encoding='UTF-8', mode='r').read().split('\n')
    print(file_read)
    score = 0
    vremya = 0.0
    best_score = int(file_read[4])
    best_time = float(file_read[5])
    total_score = 0
    time_bonus = 0
    played = int(file_read[6])
    won = int(file_read[7])
    pers = int(file_read[8])

    begin = pygame.time.get_ticks()
    done = False
    running = True
    playing = True
    played += 1
    pygame.display.set_caption("Solitaire")
    suits = ["clubs", "spades", "hearts", "diamonds"]

    names = ["ace", "2", "3", "4", "5", "6",
             "7", "8", "9", "10", "jack", "queen",
             "king"]

    card_dict = {}

    button1 = pygame.Rect(10, 610, 100, 50)
    button2 = pygame.Rect(690, 610, 100, 50)

    for card in names:
        for suit in suits:
            img = pygame.image.load("data/" + card + "_" + suit + ".png").convert()
            card_dict[card + "_" + suit] = img

    card_list = shuffle_cards()
    deck_list = [Deck_2(130, 30), Deck_1(30, 160), Deck_1(130, 160), Deck_1(230, 160),
                 Deck_1(330, 160), Deck_1(430, 160), Deck_1(530, 160), Deck_1(630, 160),
                 Deck_3(330, 30), Deck_3(430, 30), Deck_3(530, 30), Deck_3(630, 30)]

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

    start_screen()

    while not done:
        pos = pygame.Rect([i - 1 for i in pygame.mouse.get_pos()], [2, 2])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in deck_list:
                    item.click_down(m_card)

            if event.type == pygame.MOUSEBUTTONUP:
                m_card.click_up(deck_list)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pos.colliderect(button1):
                    played += 1
                    print(played)
                    main()
                if pos.colliderect(button2):
                    if playing:
                        pygame.mixer.music.stop()
                        pygame.draw.rect(screen, GREEN if not pos.colliderect(button2) else GRAY, button2)
                        screen.blit(pygame.font.SysFont(fnt, 20).render(TEXT[3], True, BLACK), [696, 590])
                        playing = False
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        playing = True

        for item in deck_list:
            if isinstance(item, Deck_3):
                if len(item.cards) != 13:
                    break
        else:
            game_over = True
            if game_over:
                won += 1
                fin = pygame.time.get_ticks()
                vremya = (fin - begin) / 1000
                if total_score > best_score:
                    best_score = total_score
                if vremya < best_time:
                    best_time = vremya
                file_write = open('statistics.txt', encoding='UTF-8', mode='w')
                file_write.seek(0)
                file_write.truncate()
                file_read[0] = score
                file_read[1] = vremya
                file_read[2] = time_bonus
                file_read[3] = total_score
                file_read[4] = best_score
                file_read[5] = best_time
                file_read[6] = played
                file_read[7] = won
                file_read[8] = int(played / won)
                for elem in file_read:
                    file_write.write(elem)
                finish_screen()
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                            running = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            for item in deck_list:
                                item.click_down(m_card)

                        if event.type == pygame.MOUSEBUTTONUP:
                            m_card.click_up(deck_list)
        screen.fill((0, 100, 0))
        # статистика
        pygame.draw.rect(screen, GREEN if not pos.colliderect(button1) else GRAY, button1)
        screen.blit(pygame.font.SysFont(fnt, 20).render(TEXT[1], True, BLACK), [16, 620])

        pygame.draw.rect(screen, GREEN if not pos.colliderect(button2) else GRAY, button2)
        screen.blit(pygame.font.SysFont(fnt, 20).render(TEXT[2], True, BLACK), [696, 620])

        for item in deck_list:
            item.draw_card(screen, card_dict)
        m_card.draw(screen, card_dict)
        if game_over:
            pygame.draw.rect(screen, TEAL, [0, 0, 1000, 1000])
            screen.blit(pygame.font.SysFont(fnt, 35).render(TEXT[0], True, BLACK), [250, 250])
        pygame.display.flip()

        clock.tick(20)

    terminate()


if __name__ == '__main__':
    main()
