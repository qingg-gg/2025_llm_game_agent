"""
管理遊戲狀態：
    1. 儲存玩家與 NPC 的狀態資訊、特殊的物品或任務狀態、遊戲是否結束與結局種類
    2. 將狀態轉為字典，提供 Agent 使用
    3. 將狀態轉換為文字，提供 Console 顯示
"""

class GameState:
    """管理遊戲狀態，儲存所有遊戲數據"""
    def __init__(self):
        # 玩家：位置、體力、理智、物品、是否想起真相
        self.player_location = "教室"
        self.player_health = 10
        self.player_sanity = 5
        self.player_remember = False

        # NPC A：理智、請求次數、對話次數、衝動行為、提出疑問
        self.npc_a = {
            "location": "教師辦公室",
            "sanity": 3,
            "wait_for_response": False,
            "help_count": 0,
            "talk_count": 0,
            "collapsed": False
        }

        # NPC B：理智、對話次數、衝動行為、提出疑問
        self.npc_b = {
            "location": "福利社",
            "sanity": 3,
            "talk_count": 0,
            "collapsed": False
        }

        # NPC C：理智、與他人對話次數、衝動行為、真面目
        self.npc_c = {
            "location": "圖書館",
            "sanity": 5,
            "other_talk_count": 0,
            "collapsed": False,
            "true_color": False
        }

        # 物品與任務狀態
        self.inventory = []
        self.open_classroom = False     # 第一次離開教室需使用鑰匙
        self.find_microphone = False    # Ａ提出的第四個請求要到教室拿麥克風
        self.num_bread = 3              # 麵包只有三個
        self.ask_c = False              # 是否向Ｃ提問過

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

    def get_state_dict(self):
        """將狀態轉換為文字"""
        return {
            "location": self.player_location,
            "health": self.player_health,
            "max_health": 10,
            "sanity": self.player_sanity,
            "max_sanity": 5,
            "inventory": self.inventory.copy(),
            "npc_a_sanity": self.npc_a["sanity"],
            "npc_b_sanity": self.npc_b["sanity"],
            "npc_c_sanity": self.npc_c["sanity"],
            "npc_a_collapsed": self.npc_a["collapsed"],
            "npc_b_collapsed": self.npc_b["collapsed"],
            "npc_c_collapsed": self.npc_c["collapsed"]
        }