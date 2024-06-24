import pygame
import random
from sprites import Spritesheet

class Deck:
  card_width = 113
  card_height = 125

  def __init__(self, file):
    self.sheet = Spritesheet("./assets/card_sprites.png")
    self.deck = []
    self.deck_ref = dict()
    self.create_deck_ref()
    self.reset()

  def create_deck_ref(self):
    for idx, i  in enumerate(['C', 'D', 'H', 'S']):
      for jdx, j in enumerate(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']):
        self.deck_ref[f'{i}{j}'] = [idx, jdx]
  
  def reset(self):
    self.deck = list(self.deck_ref.keys())
    random.shuffle(self.deck)
  
  def get_card(self, card):
    coords = [0, 0]
    if card == 'H':
      coords = [1, 13]
    else:
      coords = self.deck_ref[card]
    return self.sheet.get_sprite(coords[1] * self.card_width, coords[0] * self.card_height, self.card_width, self.card_height)

  def draw(self, number):
    cards = []
    for i in range(number):
      print(self.deck)
      if len(self.deck) <= 15:
        random.shuffle(self.deck)
      card = self.deck.pop()
      cards.append(card)
    return cards
