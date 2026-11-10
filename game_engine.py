"""
游戏引擎模块
"""

from card import Deck
from player import HumanPlayer, AIPlayer
from hand_evaluator import HandEvaluator

class GameEngine:
    def __init__(self, num_players=4, initial_chips=1000):
        self.num_players = num_players
        self.initial_chips = initial_chips
        self.players = []
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.dealer_position = 0
        self.current_player = 0
        self.game_phase = 'preflop'
        
        self._initialize_players()
    
    def _initialize_players(self):
        self.players = []
        human_player = HumanPlayer("玩家", self.initial_chips)
        self.players.append(human_player)
        
        ai_names = ["AI-阿尔法", "AI-贝塔", "AI-伽马"]
        for i in range(self.num_players - 1):
            ai_player = AIPlayer(ai_names[i], 'medium', self.initial_chips)
            self.players.append(ai_player)
    
    def start_new_hand(self):
        self.deck.reset()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.game_phase = 'preflop'
        
        for player in self.players:
            player.reset_round()
        
        self._deal_hole_cards()
        return self._get_game_state()
    
    def _deal_hole_cards(self):
        for player in self.players:
            cards = self.deck.deal_cards(2)
            player.receive_cards(cards)
    
    def make_player_action(self, action, amount=0):
        player = self.players[self.current_player]
        
        if action == 'fold':
            player.fold()
        elif action == 'call':
            player.call(amount)
            self.pot += amount
        elif action == 'raise':
            player.raise_bet(amount)
            self.pot += amount
            self.current_bet += amount
        
        self._next_player()
        return self._get_game_state()
    
    def _next_player(self):
        self.current_player = (self.current_player + 1) % self.num_players
    
    def _get_game_state(self):
        return {
            'players': self.players,
            'current_player': self.current_player,
            'community_cards': self.community_cards,
            'pot': self.pot,
            'game_phase': self.game_phase
        }
    
    def get_valid_actions(self):
        player = self.players[self.current_player]
        if player.is_folded:
            return []
        return ['fold', 'call', 'raise'] 