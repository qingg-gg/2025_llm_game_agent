"""
Console UI 實作：
     1. Concole 日誌方法，用於確認功能是否正常運行
     2. 設定 API 資訊
     3. 顯示標題、開場、狀態、結尾
     4. 控制遊戲流程
"""

import sys

from src.repository.game_assemble import GameAssemble
from src.ui.console.colors import Color

class ConsoleUI:
    """Console 版使用者介面"""
    def __init__(self):
        self.game = None

    def console_logger(self, level: str, message: str):
        """Console 日誌方法"""
        if level == "【ENGINE】":
            Color.print_colored(f"{level}　{message}", Color.RED)
        elif level == "【API】":
            Color.print_colored(f"{level}　{message}", Color.GREEN)
        elif level == "【PARSER】":
            Color.print_colored(f"{level}　{message}", Color.YELLOW)
        elif level == "【NARRATOR】":
            Color.print_colored(f"{level}　{message}", Color.BLUE)
        elif level == "【PROCESS】":
            Color.print_colored(f"{level}　{message}", Color.MAGENTA)

    def show_title(self):
        """顯示標題"""
        print("\n" + "=" * 60)
        Color.print_colored("文字冒險遊戲", Color.BOLD + Color.CYAN)
        Color.print_colored("計算理論　期末報告", Color.CYAN)
        print("=" * 60 + "\n")

    def setup_game(self):
        """設定遊戲"""
        Color.print_colored("請輸入所需資訊", Color.CYAN)
        api_url = input("請輸入 API 網址：").strip()
        api_key = input("請輸入 API Key：").strip()
        print()

        Color.print_colored("API 設定完成", Color.CYAN)

        # 建立遊戲
        self.game = GameAssemble(api_key = api_key, api_url = api_url, logger = self.console_logger)
        print()
        input("按 Enter 開始遊戲...")

    def show_intro(self):
        """顯示開場"""
        # 遊戲背景
        intro_text = self.game.get_intro_text()
        Color.print_colored(intro_text, Color.WHITE)

        # 初始狀態
        state = self.game.engine.state.get_state_dict()
        self.show_status(state)

        Color.print_colored("可以輸入文字來進行操作（如：「去圖書館」、「和 A 聊天」、「吃麵包」，輸入「exit」或「結束」則結束遊戲）。", Color.CYAN)

    def show_status(self, state: dict):
        """顯示狀態"""
        inventory_list = "、".join(state["inventory"]) if state["inventory"] else "無"
        status_text = f"位置：{state["location"]}\n體力：{state["health"]} / {state["max_health"]}\n理智：{state["sanity"]} / {state["max_sanity"]}\n物品：{inventory_list}\n"

        Color.print_colored(status_text, Color.YELLOW)

    def show_ending(self, ending: str):
        ending_text = self.game.get_ending_text(ending)
        print()
        Color.print_colored(ending_text["title"], Color.CYAN + Color.BOLD)
        Color.print_colored(ending_text["description"], Color.WHITE)
        print()

    def game_loop(self):
        """遊戲循環"""
        while not self.game.engine.state.game_over:
            try:
                user_input = Color.prompt_color("\n請輸入行動：", Color.YELLOW + Color.BOLD)
                user_input = user_input.strip()

                if not user_input:
                    continue
                if user_input.lower in ["exit", "quit", "退出", "結束"]:
                    Color.print_colored("\n遊戲結束。", Color.CYAN)
                    break

                print()
                result = self.game.process_input(user_input)
                Color.print_colored(result["story"], Color.WHITE)
                print()
                if not result["game_over"]:
                    self.show_status(result["game_state"])

            except KeyboardInterrupt:
                print()
                Color.print_colored("【CONSOLE】　操作受中斷。", Color.CYAN)
                break
            except Exception as e:
                print()
                Color.print_colored("【CONSOLE】　發生錯誤。\n錯誤訊息：{e}", Color.CYAN)
                Color.print_colored("請重新輸入，或輸入「quit」退出。", Color.CYAN)
                continue

        if self.game.engine.state.ending:
            self.show_ending(self.game.engine.state.ending)

    def run(self):
        """執行程式"""
        self.show_title()
        self.setup_game()
        self.show_intro()
        self.game_loop()

def main():
    """主程式"""
    try:
        ui = ConsoleUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n")
        Color.print_colored("【CONSOLE】　程式已終止。", Color.CYAN)
        sys.exit(0)

if __name__ == "__main__":
    main()