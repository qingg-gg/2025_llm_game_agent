"""
Narrator agent（根據遊戲狀態與行動結果產生故事）：
    1. 根據遊戲狀態與行動結果，呼叫 LLM 後回傳文本
    2. 回傳預設內容
"""

import textwrap

from src.repository.core.state import GameState
from src.repository.llm.base_model import BaseAgent

class NarratorAgent(BaseAgent):
    """Narrator agent，根據前的遊戲狀態和行動結果產生故事"""
    def generate_story(self, game_state: GameState, action_result: str) -> str:
        """生成並回傳敘事文本"""
        sanity_suffix = ""
        if game_state.player_sanity <= 1:
            sanity_suffix = "\n你感覺腦子亂七八糟，不知道如何思考才是對的，集中精神變得異常困難。"
        elif game_state.player_sanity <= 2:
            sanity_suffix = "\n你覺得自己精神有點恍惚，似乎快分不清什麼是真實的、什麼是腦中的聲響。"

        # 呼叫 LLM
        prompt = textwrap.dedent(f"""
            你是一個遊戲文本的生成助理，負責根據遊戲狀態與行動結果，使用繁體中文撰寫合理且一致的故事描述。
            
            當前遊戲狀態如下：
            - 玩家所在位置：{game_state.player_location}
            - 玩家體力：{game_state.player_health} / 10
            - 玩家理智：{game_state.player_sanity} / 5
            - NPC A 理智：{game_state.npc_a['sanity']} / 3 （是否發生異樣：{game_state.npc_a['collapsed']}）
            - NPC B 理智：{game_state.npc_b['sanity']} / 3 （是否發生異樣：{game_state.npc_b['collapsed']}）
            - NPC C 理智：{game_state.npc_c['sanity']} / 5 （是否發生異樣：{game_state.npc_c['collapsed']}）
            
            玩家行動的結果：
            {action_result}
            
            請根據「玩家理智值」調整敘事語氣，生成約 100 字連貫的故事描述，但不可以提到「理智值」：
            - 理智值為 4 ~ 5：語氣平靜、清楚，偏向客觀描述
            - 理智值為 2 ~ 3：開始出現不安、遲疑或對環境的懷疑
            - 理智值為 0 ~ 1：語言壓抑、扭曲，充滿恐懼或對現實感崩解的感受
            
            敘事規則：
            - 使用第三人稱或貼近玩家感受的敘事角度，但不要直接評論數據，比如數值的高低
            - 不要使用條列或項目符號
            - 請以自然段落輸出
            - 只回傳故事文本，不要包含任何說明或標記
            - 不要使用在行動中沒有提及的人名
            - 如果人名（A、B、C）出現在行動結果中，請在句子中提及
            - 如果行動結果中出現「A 詢問你」，請用一句話讓 A 提出問題
        """)
        self._log("【NARRATOR】", "生成敘事...")
        response = self.call_api(prompt, temperature = 0.3)

        if response is None:
            self._log("【NARRATOR】", "生成失敗，使用預設文本。")
            return action_result + sanity_suffix

        self._log("【NARRATOR】", "生成成功！")
        return response.strip() + sanity_suffix