"""
Agent 基礎類別：
    1. 呼叫 LLM 並回傳回應（呼叫失敗則回傳 None）
    2. 回傳預設內容，由 Parser 與 Narrayor 實作
"""

import json
import requests
from typing import Optional

from src.ui.console import Color


class BaseAgent:
    """Agent 的基礎類別，為 Parser 與 Narrator 的原型"""
    def __init__(self, api_url: str, api_key: str, test: bool = False):
        self.api_url = api_url
        self.api_key = api_key
        self.test = test

    def call_api(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """呼叫 LLM，如果呼叫失敗會回傳 None"""
        if self.test:
            return self._mock_response(prompt)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "gemma3:4b",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "stream": False
            }
            Color.print_colored("【呼叫 LLM 中...】", Color.CYAN)
            response = requests.post(self.api_url, headers = headers, json = data, timeout = 30)
            response.raise_for_status()
            result = response.json()
            Color.print_colored("【回應成功！】", Color.GREEN)
            return result["response"]

        except requests.exceptions.Timeout:
            Color.print_colored("【回應超時。】", Color.RED)
            return None
        except requests.exceptions.RequestException as e:
            Color.print_colored(f"【網路錯誤】 {e}", Color.RED)
            return None
        except json.JSONDecodeError as e:
            Color.print_colored(f"【JSON 解析錯誤】 {e}", Color.RED)
            return None
        except Exception as e:
            Color.print_colored(f"【未知錯誤】 {e}", Color.RED)
            return None

    def _mock_response(self, prompt: str) -> str:
        """不呼叫 LLM，回傳預設內容，由子類別實作"""
        pass