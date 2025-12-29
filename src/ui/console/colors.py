"""
Console 版介面設定：
    1. 透過顏色區分不同訊息
    2. 印出有文字的顏色
    3. 為輸入提示著色
"""

class Color:
    """定義文字顏色"""
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"

    @staticmethod
    def print_colored(text: str, color: str):
        """印出有顏色的文字"""
        print(f"{color}{text}{Color.RESET}")

    @staticmethod
    def prompt_color(text: str, color: str):
        """為輸入提示著色"""
        return input(f"{color}{text}{Color.RESET}")