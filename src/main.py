"""
程式進入點：
    1. 設定 API 資訊
    2. 選擇要使用的介面
"""

import sys
import os
import subprocess

from src.ui.console.console import main as console_main

def run_console():
    """執行 Console 模式"""
    print("使用終端機介面⋯⋯")
    console_main()

def run_streamlit():
    """執行 Console 模式"""
    print("使用網頁介面⋯⋯")

    path = os.path.join(os.path.dirname(__file__), "ui/web/streamlit.py")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", path])
    except Exception as e:
        print(f"無法起動 Streamlit\n錯誤訊息：{e}")


def main():
    """主程式"""
    print("歡迎光臨！")
    mode = int(input("請選擇顯示方式（1 為終端機介面、2 為網頁介面）："))

    if mode == 1:
        run_console()
    else:
        run_streamlit()

if __name__ == "__main__":
    main()