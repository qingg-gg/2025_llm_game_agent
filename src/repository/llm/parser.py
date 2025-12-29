"""
Parser agent（解析玩家的自然語言）：
    1. 解析玩家指令，呼叫 LLM 後回傳 JSON
    2. 回傳預設內容
"""

import json
import textwrap
from typing import Dict, Any

from src.repository.llm.base_model import BaseAgent

class ParserAgent(BaseAgent):
    """Parser agent，將玩家的自然語言解析為結構化指令"""
    def parse_input(self, user_input: str) -> Dict[str, Any]:
        """解析玩家輸入，並回傳結構化指令字典"""

        prompt = textwrap.dedent(f"""
            你是一個遊戲指令的解析助理，負責將玩家的自然語言轉換為結構化的遊戲指令。

            請根據玩家的語意，產生最合理的一個指令，並使用以下 JSON 結構之一：
            - {{"action": "move", "target": "<地點名稱>"}}
            - {{"action": "explore"}}
            - {{"action": "talk", "target": "<NPC 代號或名稱>"}}
            - {{"action": "use", "object": "<物品名稱>"}}
            - {{"action": "choose", "choice": "<是否接受>"}}

            說明：
            - "action" 為固定的英文單字，只能使用 "move"、"explore"、"talk"、"use"、"choose" 其中之一
            - "target"、"object" 請直接使用玩家輸入中出現的名稱或稱呼
            - "choice" 請依照玩家的語意使用 "接受" 或 "拒絕"
            - 不需要檢查該地點、NPC 或物品是否存在
            - 不需要嘗試將名稱翻譯成英文或內部代碼

            範例（僅供理解，不代表唯一合法值）：
            - 「去教室」的結構化指令為 {{"action": "move", "target": "教室"}}
            - 「跟老師說話」的結構化指令為 {{"action": "talk", "target": "老師"}}
            - 「使用鑰匙開門」的結構化指令為 {{"action": "use", "object": "鑰匙"}}
            - 「拒絕老師」的結構化指令為 {{"action": "choose", "choice": "拒絕"}}

            玩家輸入：「{user_input}」

            請只回傳 JSON 格式的指令，不要包含任何其他文字、補充說明或 Markdown 標記。
        """)
        self._log("【PARSER】", "解析語句...")
        response = self.call_api(prompt, temperature = 0.3)

        if response is None:
            self._log("【PARSER】", "解析失敗，使用預設指令。")
            return {"action": "invalid"}

        try:
            clean_response = response.replace("```json", "").replace("```", "").strip()
            if not clean_response:
                self._log("【PARSER】", f"JSON 解析失敗，回應為空字串。\n原始回應{repr(response)}")

            command = json.loads(clean_response)
            self._log("【PARSER】", f"解析成功！\n解析結果：{command}")
            return command

        except json.JSONDecodeError as e:
            self._log("【PARSER】", f"JSON 解析失敗。\n原始回應{repr(response)}")
            return {"action": "invalid"}