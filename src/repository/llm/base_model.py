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
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def call_api(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """呼叫 LLM，如果呼叫失敗會回傳 None"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "gemma3:4b",
                "prompt": prompt,
                "temperature": temperature,
                "stream": True
            }
            Color.print_colored("【呼叫 LLM 中...】", Color.CYAN)
            response = requests.post(self.api_url, headers = headers, json = data, stream = True, timeout = (10, 60))
            response.raise_for_status()
            chunks = []
            for line in response.iter_lines(decode_unicode = True):
                if not line:
                    continue
                data = json.loads(line)
                delta = data.get("response")
                if delta:
                    chunks.append(delta)
                if data.get("done"):
                    break
            return "".join(chunks)

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