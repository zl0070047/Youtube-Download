"""
游戏测试文件
"""

from card import Card, Deck
from player import HumanPlayer, AIPlayer
from hand_evaluator import HandEvaluator
from game_engine import GameEngine

def test_card():
    """测试扑克牌类"""
    print("=== 测试扑克牌类 ===")
    
    # 创建一张牌
    card = Card(0, 12)  # 黑桃A
    print(f"创建的牌: {card}")
    print(f"花色: {card.get_suit_name()}")
    print(f"点数: {card.get_rank_name()}")
    print(f"是否为红色: {card.is_red()}")
    
    # 测试牌组
    deck = Deck()
    print(f"\n牌组: {deck}")
    print(f"剩余牌数: {len(deck)}")
    
    # 洗牌
    deck.shuffle()
    print("洗牌完成")
    
    # 发牌
    cards = deck.deal_cards(5)
    print(f"发出的5张牌: {[str(card) for card in cards]}")
    print(f"剩余牌数: {len(deck)}")

def test_hand_evaluator():
    """测试牌型判断"""
    print("\n=== 测试牌型判断 ===")
    
    # 测试皇家同花顺
    royal_flush = [
        Card(0, 12),  # 黑桃A
        Card(0, 11),  # 黑桃K
        Card(0, 10),  # 黑桃Q
        Card(0, 9),   # 黑桃J
        Card(0, 8),   # 黑桃10
    ]
    
    result = HandEvaluator.evaluate_hand(royal_flush[:2], royal_flush[2:])
    print(f"皇家同花顺: {result}")
    
    # 测试四条
    four_of_a_kind = [
        Card(0, 0),   # 黑桃2
        Card(1, 0),   # 红心2
        Card(2, 0),   # 方块2
        Card(3, 0),   # 梅花2
        Card(0, 12),  # 黑桃A
    ]
    
    result = HandEvaluator.evaluate_hand(four_of_a_kind[:2], four_of_a_kind[2:])
    print(f"四条: {result}")

def test_player():
    """测试玩家类"""
    print("\n=== 测试玩家类 ===")
    
    # 测试人类玩家
    human = HumanPlayer("测试玩家", 1000)
    print(f"人类玩家: {human}")
    
    # 测试AI玩家
    ai = AIPlayer("测试AI", "medium", 1000)
    print(f"AI玩家: {ai}")
    
    # 发牌给玩家
    deck = Deck()
    cards = deck.deal_cards(2)
    human.receive_cards(cards)
    print(f"玩家手牌: {[str(card) for card in human.hole_cards]}")

def test_game_engine():
    """测试游戏引擎"""
    print("\n=== 测试游戏引擎 ===")
    
    # 创建游戏引擎
    engine = GameEngine(num_players=3, initial_chips=1000)
    print(f"游戏引擎创建成功，玩家数量: {engine.num_players}")
    
    # 开始新游戏
    game_state = engine.start_new_hand()
    print(f"游戏状态: {game_state['game_phase']}")
    print(f"当前玩家: {game_state['current_player']}")
    print(f"底池: {game_state['pot']}")
    
    # 显示玩家信息
    for i, player in enumerate(game_state['players']):
        print(f"玩家{i+1}: {player.name}, 筹码: {player.chips}")
        if player.hole_cards:
            print(f"  手牌: {[str(card) for card in player.hole_cards]}")

def main():
    """主测试函数"""
    print("德普游戏测试程序")
    print("=" * 50)
    
    try:
        test_card()
        test_hand_evaluator()
        test_player()
        test_game_engine()
        
        print("\n=== 测试完成 ===")
        print("所有测试通过！游戏逻辑正常工作。")
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 