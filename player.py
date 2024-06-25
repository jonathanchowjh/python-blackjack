import pygame
import random
from deck import Deck

location_table = {
  0: (550, 60),
  1: (550, 500),
  2: (900, 500),
  3: (200, 500),
}

class Player:
  def __init__(self, player) -> None:
    self.player = player
    self.player_state = 'PLAYING'   # playing / busted / ace / won
    self.location = location_table[player]
    self.cards = []
    self.bet_amount = 0
    self.points = 0
    self.active_buttons = []

  def get_initial_cards(self, deck: Deck):
    draw = deck.draw(2)
    for card in draw:
      self.cards.append(card)
  
  def draw_single(self, deck: Deck):
    draw = deck.draw(1)
    for card in draw:
      self.cards.append(card)

  def draw_player(self, deck: Deck, screen: pygame.Surface, game_state: str):
    # DRAW CARDS
    draw_list = self.cards.copy()
    if (self.player == 0 and game_state != 'END' and len(draw_list) > 1):
      draw_list[0] = 'H'
    for idx, card in enumerate(draw_list):
      screen.blit(deck.get_card(card), (self.location[0] + idx * 70, self.location[1] + idx * 10))
    # DRAW BET
    if (self.bet_amount != 0):
      font = pygame.font.SysFont(None, 50)
      text = font.render(f'{self.bet_amount}', True, (255, 0, 0))
      circle = pygame.draw.circle(screen, (50,50,100), (self.location[0] + 100, self.location[1] + 150), 30, 30)
      screen.blit(text, text.get_rect(center = circle.center))
    # DRAW POINTS
    font = pygame.font.SysFont(None, 50)
    text = font.render(f'{self.points}', True, (255, 0, 0))
    font_small = pygame.font.SysFont(None, 20)
    text_small = font_small.render(f'points', True, (255, 0, 0))
    circle = pygame.draw.circle(screen, (100,0,100), (self.location[0] + 20, self.location[1] + 150), 30, 30)
    screen.blit(text, text.get_rect(center = circle.center))
    screen.blit(text_small, text_small.get_rect(center = (circle.center[0], circle.center[1] + 20)))
    # DRAW BUTTONS
    for idx, button in enumerate(self.active_buttons):
      y_axis = -150
      if button['key'] == 'next_game':    # position dealer button lower
        y_axis = 200
      font = pygame.font.SysFont(None, 50)
      text = font.render(button['text'], True, (255, 0, 0))
      button_rect = pygame.Rect(self.location[0] + 20, self.location[1] + y_axis + idx * 60, 150, 50)
      pygame.draw.rect(screen, (50,50,100), button_rect)
      screen.blit(text, text.get_rect(center = button_rect.center))
      button['button_rect'] = button_rect
  
  def event_check(self, event, deck: Deck, dealer):
    for button in self.active_buttons:
      if 'button_rect' not in button.keys():
        return ''
      if button['button_rect'].collidepoint(event.pos):
        if button['key'] == 'bet':
          self.bet()
          self.remove_buttons()
          return 'bet'
        if button['key'] == 'hit':
          self.hit(deck, dealer)
          self.remove_buttons()
          return 'hit'
        if button['key'] == 'stay':
          self.stay()
          self.remove_buttons()
          return 'stay'
        if button['key'] == 'next_game':
          self.remove_buttons()
          return 'GAME_START'
    return ''

  def add_button(self, text: str, key: str):
    self.active_buttons.append({ 'text': text, 'key': key })
  
  def remove_buttons(self):
    self.active_buttons = []

  def bet(self):
    self.bet_amount += 10

  def hit(self, deck: Deck, dealer):
    draw = deck.draw(1)
    for card in draw:
      self.cards.append(card)
    won_points = self.check_win_condition(dealer.cards, 'HIT')
    dealer.points -= won_points

  def stay(self):
    pass

  def do_game_end(self, dealer, deck):
    if self.player == 0:
      return
    dealer_total = Player.get_card_total(dealer.cards)
    while dealer_total < 17:
      dealer.draw_single(deck)
      dealer_total = Player.get_card_total(dealer.cards)
    won_points = self.check_win_condition(dealer.cards, 'END')
    dealer.points -= won_points

  def check_win_condition(self, dealer, state):
    player_total = Player.get_card_total(self.cards)
    dealer_total = Player.get_card_total(dealer)
    if player_total == 21:
      won_points = self.bet_amount * 1.5
      self.points += won_points
      self.bet_amount = 0
      self.player_state = 'ACE'
      return won_points
    if player_total > 21:
      won_points = -self.bet_amount
      self.points += won_points
      self.bet_amount = 0
      self.player_state = 'BUSTED'
      return won_points
    if state == 'HIT':
      return 0
    if dealer_total == player_total:
      won_points = 0
      self.bet_amount = 0
      self.player_state = 'DRAW'
      return won_points
    if dealer_total < player_total or dealer_total > 21:
      won_points = self.bet_amount
      self.points += won_points
      self.bet_amount = 0
      self.player_state = 'WON'
      return won_points
    if dealer_total > player_total:
      won_points = -self.bet_amount
      self.points = won_points
      self.bet_amount = 0
      self.player_state = 'LOSS'
      return won_points
    return 0
  
  @staticmethod
  def get_card_total(cards=[]):
    total = 0
    aces = 0
    for card in cards:  # ADD POINTS
      if card[1] == 'A':
        total += 11
        aces += 1
      elif card[1] == 'J' or card[1] == 'Q' or card[1] == 'K':
        total += 10
      elif card[1].isnumeric():
        if int(card[1]) == 1:
          total += 10
        else:
          total += int(card[1])
    for i in range(aces): # Handle ACES
      if total <= 21:
        return total
      total -= 10
    return total



