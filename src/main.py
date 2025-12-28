"""
程式進入點
"""
import sys

from src.repository.game import GameAssemble
from src.ui.console import Color

def main():
    """主程式"""
    print("\n" + "=" * 50)
    Color.print_colored("【初始設定】", Color.CYAN + Color.BOLD)
    print("=" * 50 + "\n")

    # 選擇模式
    Color.print_colored("請選擇運行模式：(1) 正式模式  (2) 測試模式", Color.YELLOW)
    mode = input("請輸入 1 或 2：").strip()
    test = (mode == "2")
    if not test:
        Color.print_colored("請輸入 API 資訊：(1) 網址  (2) API Key", Color.YELLOW)
        api_url = input("(1) 網址：").strip()
        api_key = input("(2) API Key：").strip()
    else:
        api_url = "test_url"
        api_key = "test_key"
    input("\n按下 Enter 後開始遊戲")

    # 建立並啟動遊戲
    game = GameAssemble(api_url, api_key, test)
    game.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Color.print_colored("\n【程式終止】", Color.YELLOW)
        sys.exit(0)