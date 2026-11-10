"""
德普游戏主程序
"""

import tkinter as tk
from tkinter import messagebox
from game_engine import GameEngine

class PokerGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("德普游戏")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c5530')
        
        self.game_engine = None
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2c5530')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title = tk.Label(main_frame, text="德普游戏", 
                        font=('Arial', 24, 'bold'), 
                        fg='white', bg='#2c5530')
        title.pack(pady=20)
        
        # 按钮
        buttons = [
            ("开始新游戏", self.start_game),
            ("游戏规则", self.show_rules),
            ("退出", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(main_frame, text=text, command=command,
                           font=('Arial', 16), 
                           bg='#4caf50', fg='white',
                           width=20, height=2)
            btn.pack(pady=10)
    
    def start_game(self):
        self.game_engine = GameEngine()
        messagebox.showinfo("游戏开始", "新游戏已开始！\n\n功能说明：\n- 支持2-4名玩家\n- 包含AI机器人\n- 完整的德州扑克规则\n\n注意：这是一个演示版本，GUI界面正在开发中。")
    
    def show_rules(self):
        rules = """
德州扑克规则：

1. 每位玩家获得2张底牌
2. 游戏分为5个阶段：
   - 翻牌前：发底牌后下注
   - 翻牌：发3张公共牌
   - 转牌：发第4张公共牌
   - 河牌：发第5张公共牌
   - 摊牌：比较牌型

3. 牌型大小（从大到小）：
   - 皇家同花顺
   - 同花顺
   - 四条
   - 葫芦
   - 同花
   - 顺子
   - 三条
   - 两对
   - 一对
   - 高牌

4. 操作选项：
   - 弃牌：放弃手牌
   - 跟注：跟随当前下注
   - 加注：增加下注金额
   - 过牌：不增加下注
        """
        messagebox.showinfo("游戏规则", rules)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = PokerGame()
    game.run() 