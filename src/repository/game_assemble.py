"""
主遊戲類別：
    1. 處理玩家輸入到文本產出的流程
    2. 重置遊戲
    3. 取得固定文本（開場、結局）
"""

import textwrap
from typing import Optional, Callable, Dict, Any

from src.repository.core.engine import GameEngine
from src.repository.llm.narrator import NarratorAgent
from src.repository.llm.parser import ParserAgent

class GameAssemble:
    """主遊戲類別，負責整合所有元件、控制遊戲流程"""
    def __init__(self, api_url: str, api_key: str, logger: Optional[Callable[[str, str], None]] = None):
        self.engine = GameEngine()
        self.parser = ParserAgent(api_url, api_key)
        self.narrator = NarratorAgent(api_url, api_key)
        self.logger = logger or self._default_logger

    def _default_logger(self, level: str, message: str):
        """預設日誌"""
        print(f"{level}　{message}")

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """處理玩家輸入"""
        try:
            command = self.parser.parse_input(user_input)
            result = self.engine.execute_action(command)
            if self.engine.llm_response:
                story = self.narrator.generate_story(self.engine.state, result)
                if self.engine.state.npc_a["wait_for_response"]:
                    story += "\n你要接受 A 的請求嗎？還是要拒絕他？"
            else:
                story = result
                self.engine.llm_response = True
            return {
                "success": True,
                "story": story,
                "game_state": self.engine.state.get_state_dict(),
                "game_over": self.engine.state.game_over,
                "ending": self.engine.state.ending
            }
        except Exception as e:
            self.logger("【PROCESS】", f"發生錯誤。\n錯誤訊息：{e}")
            return {
                "success": False,
                "story": "請重新嘗試。",
                "game_state": self.engine.state.get_state_dict(),
                "game_over": self.engine.state.game_over,
                "ending": None
            }

    def reset(self):
        """重置遊戲"""
        self.engine = GameEngine(logger = self.logger)

    def get_intro_text(self) -> str:
        """取得開場文本"""
        return textwrap.dedent(f"""
            當你醒來時，發現自己身處一間教室中，你愣了一會兒才反應過來，這裡是你高中。
            你對自己為何出現在這裡沒有半點頭緒，也對睡著前的事毫無印象。
            而且詭譎的是，自己早已畢業，記憶中的校舍也在幾年前，因為學校關閉而被拆除了。
            
            教室看起來已經許久沒有使用，處處積灰。但黑板上，卻用死寂的白粉筆寫著幾行字：「
            　　【規則一】別睡著。
            　　【規則二】校園生活令人熟悉，但你已經畢業了。
            　　【規則三】人在不理智時，可能會做出衝動行為。
            　　【規則四】高中是製造回憶的地方，長大後可以笑著談論往事。
            」
            
            你感到不解，這些像惡作劇般的規則此時令人毛骨悚然，你告訴自己這或許只是惡作劇，卻還是默默記下它們。
            即使內心充斥疑惑與不安，你仍強壓著情緒，試圖搞清楚發生了什麼事。
        """)

    def get_ending_text(self, ending: str) -> Dict[str, str]:
        """取得結局文本"""
        endings = {
            # 想起真相
            "ending_1": {
                "title": "【結局 1】",
                "description": textwrap.dedent(f"""
                    ⋯⋯。
                    ⋯⋯。
                    ⋯⋯。
                    那天是高中的畢業典禮，你雖然早上也照常去了學校，卻沒有出現在典禮上。
                    你知道 C 不會來，因為自己也清楚，那只不過是自己的幻想罷了。
                    但他不在的話，也沒必要出席那場典禮，聽著與自己毫無連結的人們互相祝福與告別，或許他們此時會想起你、跟你說聲再見，或許你會繼續格格不入、無人在乎，不過無論何者都沒有意義。
                    你心跳得非常快，你在畏懼：如果自己再也見不到 C 該怎麼辦？
                    你只剩下他了，只有他會注視你、傾聽你、包容你，但他只出現在學校的圖書館中，或許今日踏出校門後，你就再也見不到他了。
                    現實令你恐懼、寂寞得快要瘋了，不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開、不想分開。
                    ⋯⋯如果他無法過來找自己，或許你也該為了 C 挺身一次，展現自己的誠意與決心。
                    畢竟，關係是雙向的，你沒有做錯任何事。
                """)
            },
            # 睡著
            "ending_2": {
                "title": "【結局 2】",
                "description": textwrap.dedent(f"""
                        你覺得身體非常沉重、四肢無力，眼皮難以支撐。
                        在意識逐漸遠去之際，你想起 A 常在課堂上說的：「學校是拿來學習的，要睡覺就回家再睡！」
                        雖然只是再平凡不過的日常，此時卻讓你感到些許欣慰。
                        晚安，祝你好夢。
                """)
            },
            # 自殺
            "ending_3": {
                "title": "【結局 3】",
                "description":  textwrap.dedent(f"""
                    要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了要瘋了。受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了受不了了。
                    馬上，我要逃離這裡，救我，好可怕，我不要，我不要，救我，拜託，我不要。
                    啊啊啊啊啊啊啊啊啊啊啊！！！我要馬上離開！我知道怎麼做，我很熟悉，馬上就能解脫，我知道怎麼做！
                    現在，立刻，我要解脫，我要————
                """)
            },
            # 融入
            "ending_4": {
                "title": "【結局 4】",
                "description": textwrap.dedent(f"""
                    交談間，你逐漸放下戒心，這裡似乎與你熟悉的校園別無二致。
                    是啊，你為何會感到懷疑？無論建築、綠植、眼前的人、或是自己，明明毫無突兀之處。
                    最初為什麼會產生疑惑，你早已想不起來，或許那也不是多麽重要的事。
                    現在內心那股暖流告訴你，這就是你的歸處，其他一切都不用再去多想了。
                """)
            },
            # C 生氣
            "ending_5": {
                "title": "【結局 5】",
                "description": textwrap.dedent(f"""
                    忽然，C 出現在身側，他拉了拉你的衣角，你才注意到他。
                    C 的表情看起來相當漠然，卻在眼神中蘊藏著不對勁的火光，似乎正在生氣。
                    他請你跟他出去一趟，你雖然感到些許畏懼，但不敢反抗 C，溫順地跟著他走了。
                    在一整路的靜默下，你們來到了圖書館，現在沒有任何人在。
                    「你只有我⋯⋯你只能有我，知道吧？」C 低著頭，你看不到他的表情，他的聲音非常輕，與他話語的重量形成強烈對比。
                    「⋯⋯知道。」
                    「放著我好玩嗎？離開我的人生燦爛嗎？充實嗎？有趣嗎？」C 的頭仍舊沒有抬起。
                    你沒有答覆 C，而是並上雙眼，你的直覺告訴你 C 希望你這麼做。
                    「是你讓我來陪你的，是你，搞清楚。」C 的聲音聽起來很委屈，「我也是有感受的，我和你不一樣，我只有你⋯⋯啊啊，算了。」
                    你聽到一聲嘆息，隨即感到劇烈陣痛，猛然睜眼，你看到自己的身軀已經染紅。
                    卻不見 C 的身影，彷彿他從未出現過。
                """)
            },
            # C 的真面目
            "ending_6": {
                "title": "【結局 6】",
                "description": textwrap.dedent(f"""
                    「你想起什麼了？」C 質問道，你不太明白他的意思，但這似乎令他更加煩躁。
                    C 的話語在空氣中漂浮，接著消散，氣氛陷入尷尬的死寂。
                    看著你不理解他想法、徬徨無措的模樣，C 的警戒慢慢降低，面容又再度平靜，就像平時一樣和藹可親。
                    然而他口中說出的話卻令人費解。
                    「再這樣下去也不是辦法，你讓我感到擔憂。」
                    「你一定會拋棄我的吧？我不希望你離開我。」
                    「⋯⋯不，這樣說感覺太自私了，我們重來一次。」
                    「我們是朋友吧，看著你如此難受，我心裡也覺得難過。」
                    「『如果可以代替你承擔這份重量，或許你就不會這麼痛苦了吧』我時常這樣想。」
                    下一瞬間，你感到一陣暈眩，當視野再次清晰時，你看到眼前的人，是自己。
                    而自己已經無法移動，不能轉頭，也發不出聲，像是被牢牢釘死在原地。
                    「你」看向自己，輕聲說道：「辛苦你了，好好休息。」
                    「⋯⋯這樣我們就能永遠在一起了。」
                """)
            }
        }
        return endings.get(ending, {"title": "【結局 0】", "description": "你被迫停止了思緒。"})