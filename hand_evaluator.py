"""
牌型判断模块
用于判断德州扑克的牌型大小
"""

from card import Card
from collections import Counter

class HandEvaluator:
    """牌型判断器"""
    
    # 牌型等级定义
    HAND_RANKS = {
        'high_card': 1,
        'pair': 2,
        'two_pair': 3,
        'three_of_a_kind': 4,
        'straight': 5,
        'flush': 6,
        'full_house': 7,
        'four_of_a_kind': 8,
        'straight_flush': 9,
        'royal_flush': 10
    }
    
    @staticmethod
    def evaluate_hand(hole_cards, community_cards):
        """
        评估手牌强度
        
        Args:
            hole_cards (list): 玩家的两张底牌
            community_cards (list): 公共牌
            
        Returns:
            tuple: (牌型等级, 牌型名称, 主要牌值, 次要牌值列表)
        """
        all_cards = hole_cards + community_cards
        
        # 检查各种牌型
        if HandEvaluator._is_royal_flush(all_cards):
            return (10, "皇家同花顺", 14, [])
        elif HandEvaluator._is_straight_flush(all_cards):
            return (9, "同花顺", HandEvaluator._get_straight_high(all_cards), [])
        elif HandEvaluator._is_four_of_a_kind(all_cards):
            return (8, "四条", HandEvaluator._get_four_rank(all_cards), [])
        elif HandEvaluator._is_full_house(all_cards):
            return (7, "葫芦", HandEvaluator._get_full_house_three(all_cards), [])
        elif HandEvaluator._is_flush(all_cards):
            return (6, "同花", HandEvaluator._get_flush_high(all_cards), [])
        elif HandEvaluator._is_straight(all_cards):
            return (5, "顺子", HandEvaluator._get_straight_high(all_cards), [])
        elif HandEvaluator._is_three_of_a_kind(all_cards):
            return (4, "三条", HandEvaluator._get_three_rank(all_cards), [])
        elif HandEvaluator._is_two_pair(all_cards):
            return (3, "两对", HandEvaluator._get_two_pair_high(all_cards), [])
        elif HandEvaluator._is_pair(all_cards):
            return (2, "一对", HandEvaluator._get_pair_rank(all_cards), [])
        else:
            return (1, "高牌", HandEvaluator._get_high_card(all_cards), [])
    
    @staticmethod
    def compare_hands(hand1, hand2):
        """
        比较两手牌的大小
        
        Args:
            hand1 (tuple): 第一手牌的评估结果
            hand2 (tuple): 第二手牌的评估结果
            
        Returns:
            int: 1表示hand1赢，-1表示hand2赢，0表示平局
        """
        # 比较牌型等级
        if hand1[0] > hand2[0]:
            return 1
        elif hand1[0] < hand2[0]:
            return -1
        
        # 牌型相同，比较主要牌值
        if hand1[2] > hand2[2]:
            return 1
        elif hand1[2] < hand2[2]:
            return -1
        
        # 主要牌值相同，比较次要牌值
        for i in range(min(len(hand1[3]), len(hand2[3]))):
            if hand1[3][i] > hand2[3][i]:
                return 1
            elif hand1[3][i] < hand2[3][i]:
                return -1
        
        return 0  # 完全平局
    
    @staticmethod
    def _is_royal_flush(cards):
        """判断是否为皇家同花顺"""
        if not HandEvaluator._is_flush(cards):
            return False
        
        ranks = [card.rank for card in cards]
        return all(rank in ranks for rank in [8, 9, 10, 11, 12])  # 10, J, Q, K, A
    
    @staticmethod
    def _is_straight_flush(cards):
        """判断是否为同花顺"""
        return HandEvaluator._is_flush(cards) and HandEvaluator._is_straight(cards)
    
    @staticmethod
    def _is_four_of_a_kind(cards):
        """判断是否为四条"""
        rank_counts = Counter([card.rank for card in cards])
        return 4 in rank_counts.values()
    
    @staticmethod
    def _is_full_house(cards):
        """判断是否为葫芦"""
        rank_counts = Counter([card.rank for card in cards])
        values = list(rank_counts.values())
        return 3 in values and 2 in values
    
    @staticmethod
    def _is_flush(cards):
        """判断是否为同花"""
        suits = [card.suit for card in cards]
        suit_counts = Counter(suits)
        return max(suit_counts.values()) >= 5
    
    @staticmethod
    def _is_straight(cards):
        """判断是否为顺子"""
        ranks = sorted([card.rank for card in cards])
        unique_ranks = list(set(ranks))
        
        if len(unique_ranks) < 5:
            return False
        
        # 检查普通顺子
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i+4] - unique_ranks[i] == 4:
                return True
        
        # 检查A-2-3-4-5顺子
        if 12 in unique_ranks:  # 有A
            low_ranks = [r for r in unique_ranks if r < 5]
            if len(low_ranks) >= 4 and all(r in low_ranks for r in [0, 1, 2, 3]):
                return True
        
        return False
    
    @staticmethod
    def _is_three_of_a_kind(cards):
        """判断是否为三条"""
        rank_counts = Counter([card.rank for card in cards])
        return 3 in rank_counts.values()
    
    @staticmethod
    def _is_two_pair(cards):
        """判断是否为两对"""
        rank_counts = Counter([card.rank for card in cards])
        pairs = [count for count in rank_counts.values() if count >= 2]
        return len(pairs) >= 2
    
    @staticmethod
    def _is_pair(cards):
        """判断是否为对子"""
        rank_counts = Counter([card.rank for card in cards])
        return 2 in rank_counts.values()
    
    @staticmethod
    def _get_straight_high(cards):
        """获取顺子的最高牌"""
        ranks = sorted([card.rank for card in cards])
        unique_ranks = list(set(ranks))
        
        # 检查普通顺子
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i+4] - unique_ranks[i] == 4:
                return unique_ranks[i+4]
        
        # 检查A-2-3-4-5顺子
        if 12 in unique_ranks:
            low_ranks = [r for r in unique_ranks if r < 5]
            if len(low_ranks) >= 4 and all(r in low_ranks for r in [0, 1, 2, 3]):
                return 3  # 5是最高牌
        
        return 0
    
    @staticmethod
    def _get_four_rank(cards):
        """获取四条的牌值"""
        rank_counts = Counter([card.rank for card in cards])
        for rank, count in rank_counts.items():
            if count == 4:
                return rank
        return 0
    
    @staticmethod
    def _get_full_house_three(cards):
        """获取葫芦中三条的牌值"""
        rank_counts = Counter([card.rank for card in cards])
        for rank, count in rank_counts.items():
            if count == 3:
                return rank
        return 0
    
    @staticmethod
    def _get_flush_high(cards):
        """获取同花的最高牌"""
        suits = [card.suit for card in cards]
        suit_counts = Counter(suits)
        flush_suit = max(suit_counts, key=suit_counts.get)
        
        flush_cards = [card for card in cards if card.suit == flush_suit]
        return max(card.rank for card in flush_cards)
    
    @staticmethod
    def _get_three_rank(cards):
        """获取三条的牌值"""
        rank_counts = Counter([card.rank for card in cards])
        for rank, count in rank_counts.items():
            if count == 3:
                return rank
        return 0
    
    @staticmethod
    def _get_two_pair_high(cards):
        """获取两对中较高的对子牌值"""
        rank_counts = Counter([card.rank for card in cards])
        pairs = [(rank, count) for rank, count in rank_counts.items() if count >= 2]
        pairs.sort(key=lambda x: x[0], reverse=True)
        return pairs[0][0] if pairs else 0
    
    @staticmethod
    def _get_pair_rank(cards):
        """获取对子的牌值"""
        rank_counts = Counter([card.rank for card in cards])
        for rank, count in rank_counts.items():
            if count == 2:
                return rank
        return 0
    
    @staticmethod
    def _get_high_card(cards):
        """获取高牌的最大牌值"""
        return max(card.rank for card in cards)
    
    @staticmethod
    def get_hand_description(hand_result):
        """
        获取牌型的详细描述
        
        Args:
            hand_result (tuple): 牌型评估结果
            
        Returns:
            str: 牌型描述
        """
        rank_names = ['', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        hand_name = hand_result[1]
        main_rank = hand_result[2]
        
        if hand_name == "高牌":
            return f"{hand_name} {rank_names[main_rank]}"
        elif hand_name in ["一对", "三条", "四条"]:
            return f"{hand_name} {rank_names[main_rank]}"
        elif hand_name == "两对":
            return f"{hand_name} {rank_names[main_rank]}"
        elif hand_name == "葫芦":
            return f"{hand_name} {rank_names[main_rank]}"
        else:
            return hand_name 