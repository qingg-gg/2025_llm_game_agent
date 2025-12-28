"""
Narrator agent（根據遊戲狀態與行動結果產生故事）：
    1. 根據遊戲狀態與行動結果，呼叫 LLM 後回傳文本
    2. 回傳預設內容
"""
import textwrap

from src.repository.core.state import GameState
from src.repository.llm.base_model import BaseAgent
from src.ui.console import Color


class NarratorAgent(BaseAgent):
    """Narrator agent，根據前的遊戲狀態和行動結果產生故事"""
    def generate_story(self, game_state: GameState, action_result: str) -> str:
        """生成並回傳敘事文本"""
        sanity_suffix = ""
        if game_state.player_sanity == 2:
            sanity_suffix = "\n（你感覺腦子亂七八糟，不知道如何思考才是對的，集中精神變得異常困難。）"
        elif game_state.player_sanity <= 1:
            sanity_suffix = "\n（你覺得周遭非常吵雜，就像有無數個聲音在腦中大聲咆哮，似乎快分不清什麼是真實的、什麼是腦中的聲響。）"

        # 呼叫 LLM
        prompt = textwrap.dedent(f"""
            你是一個遊戲文本的生成助理，負責根據遊戲狀態與行動結果，撰寫合理且一致的故事描述。
            
            當前遊戲狀態如下：
            - 玩家所在位置：{game_state.player_location}
            - 玩家體力：{game_state.player_health} / 10
            - 玩家理智：{game_state.player_sanity} / 5
            - NPC A 理智：{game_state.npc_a['sanity']} / 3 （是否已經崩潰：{game_state.npc_a['collapsed']}）
            - NPC B 理智：{game_state.npc_b['sanity']} / 3 （是否已經崩潰：{game_state.npc_b['collapsed']}）
            - NPC C 理智：{game_state.npc_c['sanity']} / 5 （是否已經崩潰：{game_state.npc_c['collapsed']}）
            
            玩家行動的結果：
            {action_result}
            
            請根據「玩家理智值」調整敘事語氣，生成 2 到 3 句連貫的故事描述：
            - 理智高（4 ~ 5）：語氣平靜、清楚，偏向客觀描述
            - 理智中（2 ~ 3）：開始出現不安、遲疑或對環境的懷疑
            - 理智低（0 ~ 1）：語言壓抑、扭曲，充滿恐懼或對現實感崩解的感受
            
            敘事規則：
            - 使用第三人稱或貼近玩家感受的敘事角度，但不要直接評論數據
            - 不要使用條列或項目符號
            - 請以自然段落輸出
            - 只回傳故事文本，不要包含任何說明或標記
        """)
        Color.print_colored("【Agent 生成中...】", Color.YELLOW)
        response = self.call_api(prompt, temperature = 0.7)

        if response is None:
            Color.print_colored("【生成失敗】 使用預設文本", Color.RED)
            return action_result + sanity_suffix

        Color.print_colored("【文本生成】", Color.GREEN)
        return response.strip() + sanity_suffix

    def _mock_response(self, prompt: str) -> str:
        """不呼叫 LLM，根據關鍵字回傳預設內容"""
        if "移動" in prompt:
            return "你踏入了新的區域，空氣中瀰漫陌生的氣息。"
        elif "探索" in prompt:
            return "你仔細檢查了四周，試圖找到任何線索。"
        elif "對話" in prompt:
            return "對話在空蕩的空間中發散，隨即回歸寂靜。"
        else:
            return "你完成了動作。"