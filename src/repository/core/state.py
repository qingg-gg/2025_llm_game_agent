"""
管理遊戲狀態：
    1. 儲存玩家與 NPC 的狀態資訊、特殊的物品或任務狀態、遊戲是否結束與結局種類
    2. 將狀態轉為字典，提供 Agent 使用
    3. 將狀態轉換為文字，提供 Console 顯示
"""

class GameState:
    """管理遊戲狀態，儲存所有遊戲數據"""
    def __init__(self):
        # 玩家：位置、體力、理智
        self.player_location = "教室"
        self.player_health = 10
        self.player_sanity = 5

        # NPC A：理智、請求次數、對話次數、衝動行為、提出疑問
        self.npc_a = {
            "sanity": 3,
            "help_count": 0,
            "talk_count": 0,
            "collapsed": False,
            "has_given_question": False

        }

        # NPC B：理智、對話次數、衝動行為、提出疑問
        self.npc_b = {
            "sanity": 3,
            "talk_count": 0,
            "collapsed": False,
            "has_given_question": False
        }

        # NPC C：理智、與他人對話次數、衝動行為
        self.npc_c = {
            "sanity": 5,
            "other_talk_count": 0,
            "collapsed": False
        }

        # 物品與任務狀態
        self.inventory = []
        self.has_a_question = False
        self.has_b_question = False

        # 遊戲結束狀態
        self.game_over = False
        self.ending = None

    def state_to_dictionary(self):
        """將狀態轉換為字典"""
        return {
            "player_location": self.player_location,
            "player_health": self.player_health,
            "player_sanity": self.player_sanity,
            "npc_a": self.npc_a.copy(),
            "npc_b": self.npc_b.copy(),
            "npc_c": self.npc_c.copy(),
            "inventory": self.inventory.copy(),
            "game_over": self.game_over,
            "ending": self.ending
        }

    def get_state_text(self):
        """將狀態轉換為文字"""
        inventory_str = "、".join(self.inventory) if self.inventory else "無"
        return f"【體力】 {self.player_health} / 10\n【理智】 {self.player_sanity}\n【位置】 {self.player_location}\n【物品】 {inventory_str}"