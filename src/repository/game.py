"""
主遊戲類別：
"""

import textwrap

from src.repository.core.engine import GameEngine
from src.repository.llm.narrator import NarratorAgent
from src.repository.llm.parser import ParserAgent
from src.ui.console import Color


class GameAssemble:
    """主遊戲類別，負責整合所有元件、控制遊戲流程"""
    def __init__(self, api_url: str, api_key: str, test: bool = False):
        self.engine = GameEngine()
        self.parser = ParserAgent(api_url, api_key, test)
        self.narrator = NarratorAgent(api_url, api_key, test)
        self.test = test

    def start(self):
        """開始遊戲"""
        self._show_title()
        self._show_intro_()
        self.game_loop()

    def _show_title(self):
        """顯示標題"""
        print("\n" + "=" * 50)
        Color.print_colored("文字冒險遊戲", Color.BOLD + Color.CYAN)
        Color.print_colored("計算理論　期末報告", Color.CYAN)
        print("=" * 50 + "\n")

        if self.test:
            Color.print_colored("【測試模式】 不會呼叫 LLM\n", Color.YELLOW)

    def _show_intro_(self):
        """顯示開場"""
        intro = textwrap.dedent(f"""
            當你醒來時，發現自己身處一間教室中。望向窗外，是純澈的黑，晴朗無雲，只有皎潔彎月高懸於空。
            你愣了一會兒才反應過來，這裡是你高中。
            你對自己為何出現在這裡沒有半點頭緒，也對睡著前的事毫無印象。
            而且詭譎的是，自己早已畢業，記憶中的校舍也在幾年前，因為學校關閉而被拆除了。
            
            教室貌似沒有使用的痕跡，課桌椅、置物櫃都是嶄新且空蕩的。只有黑板上，用死寂的白粉筆寫著幾行字：「
            　　【規則一】別睡著。
            　　【規則二】校園生活令人熟悉，但你已經畢業了。
            　　【規則三】人在不理智時，可能會做出衝動行為。
            　　【規則四】高中是製造回憶的地方，長大後可以笑著談論往事。
            」
            
            你感到不解，這些像惡作劇般的規則此時令人毛骨悚然，你告訴自己這或許只是惡作劇，卻還是默默記下它們。
            即使內心充斥疑惑與不安，你仍強壓著情緒，試圖搞清楚發生了什麼事。
        """)
        Color.print_colored(intro + "\n", Color.WHITE)

        guide = textwrap.dedent(f"""
            操作提示：可以使用自然語言輸入想進行的操作（輸入「exit」則結束遊戲）。
            操作範例：「去圖書館」、「和 A 聊天」、「吃麵包」。
        """)
        Color.print_colored(guide + "\n", Color.GREEN)

    def game_loop(self):
        """遊戲循環"""
        while not self.engine.state.game_over:
            try:
                # 玩家輸入操作
                user_input = Color.print_colored("\n輸入行動：", Color.BLUE + Color.BOLD)
                user_input = user_input.strip()
                if not user_input:
                    continue
                if user_input.lower() == "exit":
                    Color.print_colored("\n【遊戲結束】", Color.YELLOW)
                    break
                print()

                # 解析動作 -> 執行邏輯 -> 生成敘事
                command = self.parser.parse_input(user_input)
                result = self.engine.execute_action(command)
                story = self.narrator.generate_story(self.engine.state, result)

                # 顯示結果與狀態
                print("\n" + "=" * 50)
                Color.print_colored(story + "\n", Color.WHITE)
                if not self.engine.state.game_over:
                    Color.print_colored(self.engine.state.get_state_text(), Color.CYAN)

            except KeyboardInterrupt:
                Color.print_colored("\n【遊戲中斷】", Color.YELLOW)
                break
            except Exception as e:
                Color.print_colored(f"\n【發生錯誤】 {e}", Color.RED)
                Color.print_colored("【可做操作】 請再次嘗試，或輸入「exit」退出遊戲", Color.YELLOW)
                continue

        self._show_ending()

    def _show_ending(self):
        """顯示結局"""
        if not self.engine.state.ending:
            return

        endings = {
            "ending_1": ("【Ending 1】", "t"), # 想起真相
            "ending_2": ("【Ending 2】", "t"), # 睡著
            "ending_3": ("【Ending 3】", "t"), # 自殺
            "ending_4": ("【Ending 4】", "t"), # 融入
            "ending_5": ("【Ending 5】", "t"), # C 生氣
            "ending_6": ("【Ending 6】", "t")  # C 的真面目
        }
        title, description = endings.get(self.engine.state.ending)

        print("\n" + "=" * 50)
        Color.print_colored(title, Color.RED + Color.BOLD)
        Color.print_colored(description, Color.WHITE)
        print("=" * 50 + "\n")