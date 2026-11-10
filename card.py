"""
扑克牌类模块
定义扑克牌的基本属性和操作
"""

class Card:
    """扑克牌类"""
    
    # 花色定义
    SUITS = ['♠', '♥', '♦', '♣']
    SUIT_NAMES = ['黑桃', '红心', '方块', '梅花']
    
    # 点数定义
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    RANK_NAMES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '杰克', '皇后', '国王', 'A']
    
    def __init__(self, suit, rank):
        """
        初始化扑克牌
        
        Args:
            suit (int): 花色索引 (0-3)
            rank (int): 点数索引 (0-12)
        """
        self.suit = suit
        self.rank = rank
        self.face_up = False  # 是否正面朝上
    
    def __str__(self):
        """返回牌的字符串表示"""
        if self.face_up:
            return f"{self.SUITS[self.suit]}{self.RANKS[self.rank]}"
        else:
            return "🂠"  # 背面
    
    def __repr__(self):
        """返回牌的详细表示"""
        return f"Card({self.suit}, {self.rank})"
    
    def __eq__(self, other):
        """比较两张牌是否相等"""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        """哈希值，用于字典键"""
        return hash((self.suit, self.rank))
    
    def get_suit_name(self):
        """获取花色名称"""
        return self.SUIT_NAMES[self.suit]
    
    def get_rank_name(self):
        """获取点数名称"""
        return self.RANK_NAMES[self.rank]
    
    def get_value(self):
        """获取牌的点数值（用于比较大小）"""
        return self.rank
    
    def is_red(self):
        """判断是否为红色牌（红心、方块）"""
        return self.suit in [1, 2]  # 红心、方块
    
    def flip(self):
        """翻转牌面"""
        self.face_up = not self.face_up
    
    def show(self):
        """显示牌面"""
        self.face_up = True
    
    def hide(self):
        """隐藏牌面"""
        self.face_up = False


class Deck:
    """扑克牌组类"""
    
    def __init__(self):
        """初始化一副完整的扑克牌"""
        self.cards = []
        self.reset()
    
    def reset(self):
        """重置牌组为完整的一副牌"""
        self.cards = []
        for suit in range(4):
            for rank in range(13):
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """洗牌"""
        import random
        random.shuffle(self.cards)
    
    def deal(self):
        """发一张牌"""
        if len(self.cards) > 0:
            return self.cards.pop()
        return None
    
    def deal_cards(self, num_cards):
        """发多张牌"""
        cards = []
        for _ in range(min(num_cards, len(self.cards))):
            card = self.deal()
            if card:
                cards.append(card)
        return cards
    
    def add_card(self, card):
        """添加一张牌到牌组"""
        self.cards.append(card)
    
    def remove_card(self, card):
        """从牌组中移除一张牌"""
        if card in self.cards:
            self.cards.remove(card)
    
    def get_remaining_cards(self):
        """获取剩余牌数"""
        return len(self.cards)
    
    def is_empty(self):
        """检查牌组是否为空"""
        return len(self.cards) == 0
    
    def __str__(self):
        """返回牌组的字符串表示"""
        return f"牌组剩余 {len(self.cards)} 张牌"
    
    def __len__(self):
        """返回牌组长度"""
        return len(self.cards) 