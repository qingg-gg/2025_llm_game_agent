"""
Streamlit UI 實作：
    1. Streamlit 日誌方法，用於確認功能是否正常運行
    2. 設定 Streamlit 頁面框架、樣式、儲存資訊（Session state）
    3. 設定個元件位置與功能（）
"""

import streamlit as st
import os

from src.repository.game_assemble import GameAssemble

# 頁面框架
st.set_page_config(
    page_title = "文字冒險遊戲",
    page_icon = "🎮",
    layout = "wide",
    initial_sidebar_state = "expanded",
)

# CSS
st.markdown("""
    <style>
        [data-testid = "stMainBlockContainer"]{
            background: linear-gradient(180deg, #1a1a2e, #16213e, #0f0f1e);
            padding: 2rem 3rem 5rem
        }
        [data-testid = "stSidebar"]{background: linear-gradient(180deg, #667eea, #764ba2);}
        [data-testid = "stSidebarHeader"]{display: none;}
        [data-testid = "stHeader"]{display: none;}
    </style>
""", unsafe_allow_html = True)

def init_session_state():
    """Session state，每次頁面更新時保留的資訊"""
    ss = st.session_state
    ss.setdefault("messages", [])
    ss.setdefault("game", None)
    ss.setdefault("game_started", False)
    ss.setdefault("api_key", os.environ.get("API_KEY", ""))
    ss.setdefault("api_url", os.environ.get("API_URL", ""))

def render_sidebar():
    """Sidebar 顯示內容"""
    with st.sidebar:
        st.title("遊 戲 狀 態")

        if st.session_state.game_started and st.session_state.game:
            state = st.session_state.game.engine.state.get_state_dict()

            st.markdown(f"【 地 點 】{state["location"]}")

            st.markdown(f"【 體 力 】 {state["health"]} / {state["max_health"]}")
            st.progress(state["health"] / state["max_health"])

            st.markdown(f"【 理 智 】 {state["sanity"]} / {state["max_sanity"]}")
            st.progress(state["sanity"] / state["max_sanity"])

            st.markdown("【 物 品 】")
            if state["inventory"]:
                for item in state["inventory"]:
                    st.write("・", item)
            else:
                st.caption("無")

            st.markdown(f"【 Ａ 的 理 智 】 {state["npc_a_sanity"]} / 3")
            st.progress(state["npc_a_sanity"] / 3)

            st.markdown(f"【 Ｂ 的 理 智 】 {state["npc_b_sanity"]} / 3")
            st.progress(state["npc_b_sanity"] / 3)

            st.markdown(f"【 Ｃ 的 理 智 】 {state["npc_c_sanity"]} / 5")
            st.progress(state["npc_c_sanity"] / 5)

        else:
            st.caption("尚未開始遊戲")

        st.divider()

        with st.expander("遊 戲 選 項", expanded = True):
            st.session_state.api_key = st.text_input("API Key", value = st.session_state.api_key, type = "password")
            st.session_state.api_url = st.text_input(
                "API URL", value = st.session_state.api_url
            )
            if st.button("開 始 遊 戲", use_container_width = True):
                start_game()
            if st.button("重 置 遊 戲", use_container_width = True):
                reset_game()

def start_game():
    """選擇「開始遊戲後」的頁面更動"""
    if not st.session_state.api_key:
        st.error("請輸入 API Key。")
        return

    st.session_state.game = GameAssemble(
        api_key = st.session_state.api_key,
        api_url = st.session_state.api_url,
        logger = streamlit_logger,
    )
    st.session_state.game_started = True
    st.session_state.messages.clear()

    intro = st.session_state.game.get_intro_text()
    st.session_state.messages.append(("system", (intro + "**可以輸入文字來進行操作（如：「去圖書館」、「和 A 聊天」、「吃麵包」，輸入「exit」或「結束」則結束遊戲）。**").replace("\n", "  \n  \n")))

    st.rerun()

def reset_game():
    """選擇「重置遊戲」後的頁面更動"""
    st.session_state.game_started = False
    st.session_state.game = None
    st.session_state.messages.clear()
    st.rerun()

def process_user_input(text: str):
    """送出行動後的頁面更動"""
    st.session_state.messages.append(("user", text))

    with st.spinner("處理中⋯⋯"):
        result = st.session_state.game.process_input(text)

    st.session_state.messages.append(("system", result["story"]))

    if result["game_over"]:
        ending = st.session_state.game.get_ending_text(result["ending"])
        st.session_state.messages.append(
            ("ending", f"{ending['title']}\n\n{ending['description']}")
        )
    st.rerun()

def render_main():
    """Chatbox 顯示內容"""
    st.title("文字冒險遊戲 Interactive Fiction")
    st.caption("計算理論　期末報告")

    for role, content in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(content)

    if st.session_state.game_started and not st.session_state.game.engine.state.game_over:
        user_input = st.chat_input("輸入你的行動⋯⋯")
        if user_input:
            process_user_input(user_input.replace("\n", "  \n  \n"))

def streamlit_logger(level: str, message: str):
    """日誌方法"""
    print(f"{level}　{message}")

def main():
    init_session_state()
    render_sidebar()
    render_main()

if __name__ == "__main__":
    main()
