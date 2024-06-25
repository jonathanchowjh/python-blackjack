import pygame
from deck import Deck
from player import Player

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

class App:
  screen = None
  clock = None
  running = True
  bg = None
  players = []
  number_of_players = 3
  hit = False
  # GAMESTATES -> BET - DEAL - DRAW - END
  game_state = 'END'
  game_player = 0

  def __init__(self):
    self.setup()
    while self.running:
      self.screen.blit(self.bg, (0, 0))
      self.game_loop()
      pygame.display.flip()  # Refresh on-screen display
      self.clock.tick(FPS)
    pygame.quit()

  def setup(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()
    self.running = True
    # Class Init
    self.deck = Deck("./assets/card_sprites.png")
    self.players.append(Player(0))
    for i in range(self.number_of_players):
      self.players.append(Player(i + 1))
    # Background and Title
    pygame.display.set_caption('Python Blackjack')
    self.bg = pygame.image.load("./assets/table.jpg").convert()
    self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    self.next_turn('GAME_START')

  def game_loop(self):
    # Process player inputs.
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      # Check for the mouse button down event
      dealer = App.first(x for x in self.players if x.player == 0)
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for player in self.players:
          ret = player.event_check(event, self.deck, dealer)
          self.next_turn(ret)
    # DRAW
    for player in self.players:
      player.draw_player(self.deck, self.screen, self.game_state)

  def next_turn(self, ret):
    if ret == '':
      return
    if ret == 'hit':              # DRAW PHASE ONLY ENDS WHEN NO ONE HITS IN ONE PASS OF PLAYERS
      self.hit = True
    if ret == 'GAME_START':       # GAME START
      self.game_state = 'BET'
      self.game_player = 0        # starts with player 1, accounting for increment
      self.deck.reset()
      for player in self.players:
        player.cards = []
        player.player_state = 'PLAYING'
    if self.game_player + 1 < len(self.players):    # INCREMENT PLAYER
      self.game_player += 1
      player = App.first(x for x in self.players if x.player == self.game_player)
      if self.game_state == 'BET':
        player.add_button('Bet 5', 'bet_5')
        player.add_button('Bet 10', 'bet_10')
        player.add_button('Bet 30', 'bet_30')
        player.add_button('Bet 100', 'bet_100')
      elif player.player_state != 'PLAYING':
        self.next_turn('next_player')
      elif self.game_state == 'DRAW':
        player.add_button('Hit', 'hit')
        player.add_button('Stay', 'stay')
      return
    if self.game_state == 'BET' and self.game_player + 1 >= len(self.players):      # END OF BET PHASE
      self.game_state = 'DEAL'
      # RUN DEAL
      self.deal()
      # AUTO MOVE TO DRAW PHASE
      self.game_state = 'DRAW'
      self.game_player = 1
      self.hit = False
      player = App.first(x for x in self.players if x.player == self.game_player)
      if player.player_state != 'PLAYING':
        self.next_turn('next_player')
      else:
        player.add_button('Hit', 'hit')
        player.add_button('Stay', 'stay')
      return
    if self.game_state == 'DRAW' and self.game_player + 1 >= len(self.players):     # END OF DRAW PHASE
      still_playing = False
      for player in self.players:
        if player.player != 0 and player.player_state == 'PLAYING':
          still_playing = True
      if self.hit and still_playing:
        self.hit = False
        self.game_state = 'DRAW'
        self.game_player = 1
        player = App.first(x for x in self.players if x.player == self.game_player)
        if player.player_state != 'PLAYING':
          self.next_turn('next_player')
        else:
          player.add_button('Hit', 'hit')
          player.add_button('Stay', 'stay')
      else:
        self.game_state = 'END'
        # RUN END
        self.end()
      return

  def deal(self):
    dealer = App.first(x for x in self.players if x.player == 0)
    for player in self.players:
      player.get_initial_cards(self.deck, dealer)

  def end(self):
    dealer = App.first(x for x in self.players if x.player == 0)
    for player in self.players:
      player.do_game_end(dealer, self.deck)
    dealer.add_button('new game', 'next_game')
    pass

  @staticmethod
  def first(iterable, default=None):
    for item in iterable:
      return item
    return default

App()