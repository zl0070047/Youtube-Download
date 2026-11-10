"""
玩家类模块
"""

from card import Card
from hand_evaluator import HandEvaluator
import random

class Player:
    """玩家基类"""
    
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hole_cards = []
        self.is_folded = False
        self.is_all_in = False
        self.current_bet = 0
        self.total_bet = 0
        self.position = None
        self.is_dealer = False
        
    def receive_cards(self, cards):
        """接收底牌"""
        self.hole_cards = cards
        for card in self.hole_cards:
            card.show()
    
    def fold(self):
        """弃牌"""
        self.is_folded = True
        self.current_bet = 0
    
    def call(self, amount):
        """跟注"""
        if amount > self.chips:
            amount = self.chips
            self.is_all_in = True
        self.chips -= amount
        self.current_bet += amount
        self.total_bet += amount
    
    def raise_bet(self, amount):
        """加注"""
        if amount > self.chips:
            amount = self.chips
            self.is_all_in = True
        self.chips -= amount
        self.current_bet += amount
        self.total_bet += amount
    
    def check(self):
        """过牌"""
        pass
    
    def reset_round(self):
        """重置本轮状态"""
        self.hole_cards = []
        self.is_folded = False
        self.is_all_in = False
        self.current_bet = 0
        self.total_bet = 0
    
    def get_hand_strength(self, community_cards):
        """获取手牌强度"""
        if not self.hole_cards or self.is_folded:
            return (0, "无牌", 0, [])
        return HandEvaluator.evaluate_hand(self.hole_cards, community_cards)
    
    def can_afford(self, amount):
        """检查是否有足够筹码"""
        return self.chips >= amount
    
    def get_remaining_chips(self):
        """获取剩余筹码"""
        return self.chips
    
    def add_chips(self, amount):
        """增加筹码"""
        self.chips += amount
    
    def __str__(self):
        status = "弃牌" if self.is_folded else "游戏中"
        return f"{self.name} (筹码: {self.chips}, 状态: {status})"


class HumanPlayer(Player):
    """人类玩家类"""
    
    def __init__(self, name, chips=1000):
        super().__init__(name, chips)
        self.is_human = True
    
    def make_decision(self, game_state):
        """人类玩家做决策"""
        pass


class AIPlayer(Player):
    """AI玩家类"""
    
    def __init__(self, name, difficulty='medium', chips=1000):
        super().__init__(name, chips)
        self.difficulty = difficulty
        self.is_human = False
        self.aggression = self._get_aggression_level()
        self.bluff_frequency = self._get_bluff_frequency()
    
    def _get_aggression_level(self):
        """获取攻击性等级"""
        if self.difficulty == 'easy':
            return 0.3
        elif self.difficulty == 'medium':
            return 0.6
        else:
            return 0.8
    
    def _get_bluff_frequency(self):
        """获取诈唬频率"""
        if self.difficulty == 'easy':
            return 0.1
        elif self.difficulty == 'medium':
            return 0.2
        else:
            return 0.3
    
    def make_decision(self, game_state):
        """AI做决策"""
        hand_strength = self.get_hand_strength(game_state.get('community_cards', []))
        pot_odds = self._calculate_pot_odds(game_state)
        
        if self.difficulty == 'easy':
            return self._easy_strategy(hand_strength, game_state)
        elif self.difficulty == 'medium':
            return self._medium_strategy(hand_strength, game_state, pot_odds)
        else:
            return self._hard_strategy(hand_strength, game_state, pot_odds)
    
    def _easy_strategy(self, hand_strength, game_state):
        """简单AI策略"""
        strength = hand_strength[0]
        current_bet = game_state.get('current_bet', 0)
        min_raise = game_state.get('min_raise', 0)
        
        if strength >= 7:
            if random.random() < 0.8:
                return ('raise', min_raise * 2)
            else:
                return ('call', current_bet)
        elif strength >= 5:
            if random.random() < 0.6:
                return ('call', current_bet)
            else:
                return ('fold', 0)
        elif strength >= 3:
            if random.random() < 0.4:
                return ('call', current_bet)
            else:
                return ('fold', 0)
        else:
            if random.random() < 0.1:
                return ('call', current_bet)
            else:
                return ('fold', 0)
    
    def _medium_strategy(self, hand_strength, game_state, pot_odds):
        """中等AI策略"""
        strength = hand_strength[0]
        current_bet = game_state.get('current_bet', 0)
        min_raise = game_state.get('min_raise', 0)
        position = game_state.get('position', 'late')
        
        if strength >= 8:
            return ('raise', min_raise * 3)
        elif strength >= 6:
            if position in ['early', 'middle']:
                return ('call', current_bet)
            else:
                return ('raise', min_raise * 2)
        elif strength >= 4:
            if pot_odds > 0.3:
                return ('call', current_bet)
            elif random.random() < self.aggression:
                return ('call', current_bet)
            else:
                return ('fold', 0)
        elif strength >= 2:
            if pot_odds > 0.4 and position in ['middle', 'late']:
                return ('call', current_bet)
            elif random.random() < 0.3:
                return ('call', current_bet)
            else:
                return ('fold', 0)
        else:
            if random.random() < self.bluff_frequency and position == 'late':
                return ('call', current_bet)
            else:
                return ('fold', 0)
    
    def _hard_strategy(self, hand_strength, game_state, pot_odds):
        """困难AI策略"""
        strength = hand_strength[0]
        current_bet = game_state.get('current_bet', 0)
        min_raise = game_state.get('min_raise', 0)
        position = game_state.get('position', 'late')
        players_active = game_state.get('players_active', 1)
        
        if strength >= 9:
            return ('raise', min_raise * 4)
        elif strength >= 7:
            raise_amount = min_raise * 3 if players_active <= 2 else min_raise * 2
            return ('raise', raise_amount)
        elif strength >= 5:
            if position == 'late' and players_active <= 3:
                return ('raise', min_raise * 2)
            else:
                return ('call', current_bet)
        elif strength >= 3:
            if pot_odds > 0.25 and position in ['middle', 'late']:
                return ('call', current_bet)
            elif random.random() < 0.4:
                return ('call', current_bet)
            else:
                return ('fold', 0)
        elif strength >= 2:
            if pot_odds > 0.35 and position in ['middle', 'late']:
                return ('call', current_bet)
            elif random.random() < 0.2:
                return ('call', current_bet)
            else:
                return ('fold', 0)
        else:
            if (position == 'late' and players_active <= 2 and 
                random.random() < self.bluff_frequency):
                return ('call', current_bet)
            else:
                return ('fold', 0)
    
    def _calculate_pot_odds(self, game_state):
        """计算底池赔率"""
        current_bet = game_state.get('current_bet', 0)
        pot_size = game_state.get('pot_size', 0)
        
        if current_bet == 0:
            return 0
        
        call_amount = current_bet - self.current_bet
        if call_amount <= 0:
            return 0
        
        return call_amount / (pot_size + call_amount) 