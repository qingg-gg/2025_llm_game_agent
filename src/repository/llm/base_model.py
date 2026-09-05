"""
Agent 基礎類別：
    1. 呼叫 LLM 並回傳回應（呼叫失敗則回傳 None）
    2. 回傳預設內容，由 Parser 與 Narrator 實作
"""

import json
import requests
from typing import Optional, Callable

class BaseAgent:
    """Agent 的基礎類別，為 Parser 與 Narrator 的原型"""
    def __init__(self, api_url: str, api_key: str, logger: Optional[Callable[[str, str], None]] = None):
        self.api_url = api_url
        self.api_key = api_key
        self.logger = logger or self._default_logger

    def _log(self, level: str, message: str):
        """內部日誌方法"""
        self.logger(level, message)

    def _default_logger(self, level: str, message: str):
        """預設日誌"""
        print(f"{level}　{message}")

    def call_api(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """呼叫 LLM，如果呼叫失敗會回傳 None"""
        try:
            headers = {
                "x-goog-api-key": self.api_key,
                "Content-Type": "application/json",
            }
            data = {
                "model": "gemini-3.5-flash-lite",
                "input": prompt
            }
            self._log("【API】", "發送請求...")
            response = requests.post(self.api_url, headers = headers, json = data, timeout = (10, 60))
            response.raise_for_status()
            data = response.json()
            result = None
            for step in data["steps"]:
                if step.get("type") == "model_output":
                    result = step["content"][0]["text"]
                    break
            self._log("【API】", "回應成功！")
            return result

        except requests.exceptions.Timeout:
            self._log("【API】", "請求超時。")
            return None
        except requests.exceptions.RequestException as e:
            self._log("【API】", f"網路錯誤。\n錯誤訊息：{e}")
            return None
        except json.JSONDecodeError as e:
            self._log("【API】", f"JSON 解析錯誤。\n錯誤訊息：{e}")
            return None
        except Exception as e:
            self._log("【API】", f"未知錯誤。\n錯誤訊息：{e}")
            return None
