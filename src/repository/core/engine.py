"""
遊戲引擎：
    1. 執行所有遊戲邏輯、機制
    2. 處理玩家的行動（移動、探索、對話、使用、選擇）
    3. 檢查遊戲目前狀態（玩家、A、B、C）
    4. 特殊互動規則、機制（A、B）
"""

from typing import Dict, Any

from src.repository.core.state import GameState
from src.ui.console import Color

class GameEngine:
    """遊戲引擎，負責邏輯判斷、狀態轉換、結局判定"""
    def __init__(self):
        self.state = GameState()
        self.llm_response = True

    def execute_action(self, command: Dict[str, Any]) -> str:
        """執行遊戲指令"""
        action = command.get("action")
        Color.print_colored("【執行指令...】", Color.YELLOW)

        # 判斷指令類型
        if action == "move":
            result = self._handle_move(command.get("target", ""))
        elif action == "explore":
            result = self._handle_explore()
        elif action == "talk":
            result = self._handle_talk(command.get("target", ""))
        elif action == "use":
            result = self._handle_use(command.get("object", ""))
        elif action == "choose":
            result = self._handle_choose(command.get("choice", ""))
        else:
            self.llm_response = False
            result = "無法理解指令，請嘗試用更清楚的方式描述你的行動。"

        # 檢查特定機制是否被觸發
        self._check_self()
        self._check_npc_a()
        self._check_npc_b()
        self._check_npc_c()

        Color.print_colored(f"【完成指令】 {result[:50]}", Color.GREEN)
        return result

    def _handle_move(self, target: str) -> str:
        """處理移動指令"""
        valid_locations = ["教室", "圖書館", "福利社", "教師辦公室"]
        if self.state.player_location in valid_locations:
            valid_locations.remove(self.state.player_location)

        # 地點不存在
        if target not in valid_locations:
            self.llm_response = False
            return f"{target}是無法到達的，你能前往的地點有{valid_locations[0]}、{valid_locations[1]}、{valid_locations[2]}。"

        # 移動條件：第一次離開教室需使用鑰匙
        if not self.state.open_classroom:
            return "教室上鎖了，無法出去。「為什麼在教室裡需要鑰匙才能開鎖？」你疑惑地心想。"

        # 移動
        self.state.player_location = target
        self.state.player_health -= 1
        if self.state.npc_a["location"] == target and self.state.npc_c["location"] == target:
            return "你移動到了{target}。你看見 A 跟 C 都出現在教室。他們並沒有主動朝你攀談，而是像個擺設一樣矗立著。"
        if self.state.npc_a["location"] == target:
            return f"你移動到了{target}，你看見 A 也在這裡。教師辦公室充滿書與試卷，有很重的油墨味。"
        elif self.state.npc_b["location"] == target:
            return f"你移動到了{target}，你看見 B 也在這裡。福利社裡雖有商品陳列，但沒有其他客人，也沒有店員。"
        elif self.state.npc_c["location"] == target:
            return f"你移動到了{target}，你看見 C 也在這裡。他一個人坐在書架旁安靜地閱讀科幻小說。"
        else:
            return f"你移動到了{target}。"

    def _handle_explore(self) -> str:
        """處理探索指令"""
        self.state.player_health -= 1
        location = self.state.player_location

        # 教室
        if location == "教室":
            if not self.state.open_classroom:
                self.state.inventory.append("鑰匙")
                return "你找到了一副鑰匙，看起來與門鎖相符。"
            elif not self.state.find_microphone and self.state.npc_a["talk_count"] == 4:
                self.state.find_microphone = True
                return "你找到了 A 請你幫忙拿的麥克風，他現在在教師辦公室等你交還給他。"
            else:
                self.llm_response = False
                return "教室裡沒有什麼特別的。"

        # 圖書館
        if location == "圖書館":
            if self.state.player_sanity == 1 and "A 的疑問" in self.state.inventory and "B 的疑問" in self.state.inventory:
                self.state.inventory.append("遺書")
                self.llm_response = False
                return "你找到了一封遺書，署名是⋯⋯"
            else:
                self.llm_response = False
                return "圖書館裡沒有什麼特別的。"

        # 福利社
        if location == "福利社":
            if "麵包" not in self.state.inventory and self.state.num_bread > 0:
                self.state.num_bread -= 1
                self.state.inventory.append("麵包")
                return "你找到了一塊麵包，並且小心翼翼地收藏它。"
            else:
                self.llm_response = False
                return "福利社裡沒有什麼特別的。"

        # 教師辦公室
        else:
            return "教師辦公室裡沒有什麼特別的。"

    def _handle_talk(self, target: str) -> str:
        """處理對話指令"""
        target = target.upper()
        if target not in ["A", "B", "C"]:
            self.llm_response = False
            return f"{target}並不在校園裡，你能交談的對象有 A、B、C。"

        # A
        if target == "A" and self.state.player_location == self.state.npc_a["location"]:
            if self.state.npc_a["collapsed"]:
                self.llm_response = False
                return "A 已經不願意再與你交談了。"

            # 提出請求
            if not self.state.npc_a["wait_for_response"]:
                self.state.npc_a["talk_count"] += 1
                self.state.npc_c["other_talk_count"] += 1
                suffix = "，你思考著，還沒做出答覆。"
                match self.state.npc_a["talk_count"]:
                    case 1:
                        return self._a_request(request_id = 1) + suffix
                    case 2:
                        return self._a_request(request_id = 2) + suffix
                    case 3:
                        return self._a_request(request_id = 3) + suffix
                    case 4:
                        return self._a_request(request_id = 4) + suffix
                    case 5:
                        return self._a_request(request_id = 5) + suffix

        # B
        if target == "B"  and self.state.player_location == self.state.npc_b["location"]:
            self.state.npc_b["talk_count"] += 1
            self.state.npc_c["other_talk_count"] += 1

            match self.state.npc_b["talk_count"]:
                case 1:
                    return self._b_mood(request_id = 1)
                case 2:
                    self.state.player_sanity -= 1
                    self.state.npc_b["sanity"] -= 1
                    return self._b_mood(request_id = 2)
                case 3:
                    self.state.player_sanity -= 1
                    self.state.npc_b["sanity"] -= 1
                    return self._b_mood(request_id = 3)
                case 4:
                    self.state.player_sanity -= 1
                    self.state.npc_b["sanity"] -= 1
                    self.state.npc_a["sanity"] = 0
                    return self._b_mood(request_id = 2)
                case 5:
                    return self._b_mood(request_id = 1)

        # C
        if target == "C" and self.state.player_location == self.state.npc_c["location"]:
            self.state.npc_c["other_talk_count"] = 0
            return "C 和你介紹他正在看的書，跟 C 待在一起讓你感到非常平靜。"

        else:
            self.llm_response = False
            return f"{target} 不在這裡，你得先找到他。"

    def _handle_use(self, item: str) -> str:
        """處理使用物品指令"""
        if item not in self.state.inventory:
            self.llm_response = False
            return f"""你可以使用的物品有{"、".join(self.state.inventory)}。"""

        match item:
            case "鑰匙":
                if self.state.player_location == "教室":
                    self.state.inventory.remove(item)
                    self.state.open_classroom = True
                    return "你用鑰匙打開了教室的門，現在你終於可以離開教室了。"
            case "麵包":
                self.state.inventory.remove(item)
                self.state.player_health += 3
                if self.state.player_health > 10:
                    self.state.player_health = 10
                return "你吃麵包來填飽肚子。"
            case "考卷":
                if self.state.player_location == "教室":
                    self.state.inventory.remove(item)
                    return "你把考卷放在教室講台上。"
            case "公告":
                if self.state.player_location == "教室":
                    self.state.inventory.remove(item)
                    self.state.player_sanity -= 1
                    return "你在教室中宣布了公告，站在台上讓你感到極度焦慮。"
            case "書籍":
                if self.state.player_location == "圖書館":
                    self.state.inventory.remove(item)
                    return "你把 A 的書還給圖書館。"
            case "麥克風":
                if self.state.player_location == self.state.npc_a["location"]:
                    self.state.inventory.remove(item)
                    self.state.inventory.append("A 的疑問")
                    self.state.player_sanity -= 1
                    return "你把麥克風交給了 A，A 說他很擔心你在班上都沒有朋友，但你不理解為什麼 A 為何這麼說，明明有 C 陪伴自己啊。但你並沒有向 A 提問。"
            case "現金":
                if self.state.player_location == "福利社":
                    self.state.inventory.remove(item)
                    self.state.inventory.append("咖啡")
                    return "你幫 A 買到了咖啡。"
            case "咖啡":
                if self.state.player_location == self.state.npc_a["location"]:
                    self.state.inventory.remove(item)
                    return "你把買來的咖啡交給了 A。"
            case "A 的疑問":
                if self.state.player_location == self.state.npc_c["location"]:
                    if not self.state.ask_c:
                        self.state.inventory.remove(item)
                        self.state.ask_c = True
                        return "C 表示不理解你在說什麼，並轉移話題。"
                    else:
                        self.state.npc_c["true_color"] = True
                        return "C 一語不發地直視你，過去和藹的面容變得相當冰冷。"
            case "B 的疑問":
                if self.state.player_location == self.state.npc_c["location"]:
                    if not self.state.ask_c:
                        self.state.inventory.remove(item)
                        self.state.ask_c = True
                        return "C 表示不理解你在說什麼，並轉移話題。"
                    else:
                        self.state.npc_c["true_color"] = True
                        return "C 一語不發地直視你，過去和藹的面容變得相當冰冷。"
            case "遺書":
                if self.state.player_sanity == 1 and self.state.player_location == "教室":
                    self.state.player_remember = True
                    self.llm_response = False
                    return "你想起了一切。"
                else:
                    prefix = ""
                    self.state.npc_c["true_color"] = True
                    if self.state.npc_c["location"] != self.state.player_location:
                        self.state.npc_c["location"] = self.state.player_location
                        prefix = "C 突然出現在你面前，"
                    return prefix + "C 一語不發地直視你，過去和藹的面容變得相當冰冷。"

        self.llm_response = False
        return f"{item}並沒有發揮任何作用。"

    def _handle_choose(self, choice: str) -> str:
        """處理選擇指令"""
        if not self.state.npc_a["wait_for_response"]:
            self.llm_response = False
            return "現在沒有要回應的請求。"

        self.state.npc_a["wait_for_response"] = False
        if choice == "接受":
            self.state.npc_a["help_count"] += 1
            match self.state.npc_a["talk_count"]:
                case 1:
                    self.state.inventory.append("考卷")
                    return "A 將考卷遞給了你。"
                case 2:
                    self.state.inventory.append("公告")
                    return "A 將公告細節告訴了你。"
                case 3:
                    self.state.inventory.append("書籍")
                    return "A 將書籍遞給了你。"
                case 4:
                    return "A 告訴你麥克風大概在教室的哪邊，並說他會在教師辦公室等你拿來。"
                case 5:
                    self.state.inventory.append("現金")
                    return "A 給了你現金，讓你買兩杯，其中一杯算他請你喝的。"
        else:
            self.state.npc_a["sanity"] -= 1
            return "A 面帶失望地看著你，深深嘆了一口氣。"

    def _check_self(self):
        """確認玩家的狀態"""
        if self.state.player_remember:
            self.state.game_over = True
            self.state.ending = "ending_1"
        if self.state.player_health <= 0:
            self.state.game_over = True
            self.state.ending = "ending_2"
        if self.state.player_sanity <= 0:
            self.state.game_over = True
            self.state.ending = "ending_3"

    def _check_npc_a(self):
        """確認 A 的狀態"""
        if self.state.npc_a["sanity"] <= 0:
            self.state.npc_a["collapsed"] = True
        if self.state.npc_a["talk_count"] >= 5 or self.state.npc_a["help_count"] >= 3:
            self.state.game_over = True
            self.state.ending = "ending_4"

    def _check_npc_b(self):
        """確認 B 的狀態"""
        if self.state.npc_b["sanity"] <= 0:
            self.state.npc_b["collapsed"] = True
        if self.state.npc_b["talk_count"] >= 5:
            self.state.game_over = True
            self.state.ending = "ending_4"

    def _check_npc_c(self):
        """確認 C 的狀態"""
        if self.state.npc_c["other_talk_count"] >= 3:
            self.state.npc_c["sanity"] -= 1
        if self.state.npc_c["sanity"] <= 0:
            self.state.npc_c["collapsed"] = True
            self.state.game_over = True
            self.state.ending = "ending_5"
        if self.state.npc_c["true_color"]:
            self.state.game_over = True
            self.state.ending = "ending_6"

    def _a_request(self, request_id) -> str:
        """A 的五個請求"""
        self.state.npc_a["wait_for_response"] = True
        match request_id:
            case 1:
                return "A 請你幫他把下堂課要考的考卷拿到教室裡。"
            case 2:
                return "A 請你幫他到教室宣布一個公告。"
            case 3:
                return "A 請你幫他到圖書館歸還書籍。"
            case 4:
                return "A 把麥克風忘在教室裡了，請你幫他拿回教師辦公室。"
            case _:
                return "A 請你去福利社幫他買咖啡。"

    def _b_mood(self, request_id) -> str:
        """B 的五次談話"""
        match request_id:
            case 1:
                return "你和 B 隨意聊了些國中的事，兩個人都很懷念那段時光。"
            case 2:
                return "你和 B 聊到升高中後的事，B 認為你看起來很不快樂，想給你一些建議，但你覺得他在多管閒事，兩人不歡而散。"
            case _:
                return "B 說他時常看到你在圖書館自言自語，但你不理解為什麼 B 為何這麼說，明明自己是在跟 C 聊天啊。但你並沒有向 B 提問。"