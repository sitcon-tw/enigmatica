from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
📖 <b>前情提要</b>
【突發】SITCON創辦人康喔疑似帶走J0711黑盒子　警方已展開追查
2025年3月8日失事的J0711班機，遺骸至昨日方才全數打撈完畢。隨著搜救行動告一段落，調查作業正式進入關鍵階段，警方也已開始介入本案調查。
然而，就在今早11點55分左右，調查現場發生重大變故——根據現場目擊者指出，自稱為「SITCON創辦人」的男子康喔，突然現身於打撈調查現場，並在未經許可的情況下，將關鍵證物——J0711班機的飛航紀錄器（黑盒子）帶離現場並引發爆炸。
目前康喔下落不明，警方已發布通緝，並懷疑此舉與班機失事背後的潛在真相有所關聯。
警方呼籲，若民眾發現任何可疑行蹤，請立即通報110專線，切勿私下接觸。相關單位也將持續追查黑盒子下落，以釐清事故真相。

-

💡 <b>提示</b>
【提示 | SCYTALE】康喔跟柴柴常常傳遞一個棒子，也不確定是什麼
【提示 | GIT Denny】與康喔看著眼前的機器發呆，可能有什麼重要的線索。
【提示 | AAC】咪路在 EC329 病房看著康喔留下來的痕跡，嘆了一口氣。
【提示 | METAR】窗外下起了大雷雨，Windless看著快被悶壞的柴柴說：我們等等就會到涼快一點的地方了！雖然那邊似乎會下小雨，但能見度可是一個讚啊。 https://docs.google.com/spreadsheets/d/1IgHEe1CqywQ38NXDWRFw4pvTMX3j0xcW9EB_whIJ1QI/
【提示 | FLIGHTRADAR】Windless 看著一堆航線紀錄，整理著每個航線的資料。 
【提示 | INSTAGRAM】橘子看著 INSTAGRAM 小編發出來的訊息，持續思考著訊息的正確性，還有那藏在文字間的意涵。
【提示 | PYTHON】OsGa 看著眼前的 Python 程式，思考著如何跟股東們解釋，為什麼是 404 Not Found.
【提示 | ASCII】咪路看著眼前的密碼鎖，思考著是哪一串密碼。
【提示 | MAZE Yuan】看著眼前密密麻麻的報導，嘗試著在這堆報導迷宮中，找出一條出路。

-

🧑<b>角色說明</b>：
康喔：前Ｊ飛機公司工程師、SITCON 航空 創辦人
柴柴：前Ｊ飛機公司副機長、SITCON 航空 創辦人
Denny：前Ｊ飛機公司塔台控制人員、SITCON 創辦人
Windless：前Ｊ飛機公司塔台控制人員、SITCON 秘書
OsGa：前Ｊ飛機公司行政人員、SITCON 對外宣傳負責人
Ricky：前Ｊ飛機公司副機長
咪路：保安兼前精神病院保安
橘子：記者、前Ｊ飛機公司公關部
yuan：記者
阿六：前Ｊ公司公關部長

-

💬 <b>主要指令：</b>
• `/ans &lt;密碼&gt;` - 開始閱讀故事
• `/stories` - 查看已完成的故事
• `/start` - 顯示此幫助訊息
"""
    await update.message.reply_text(help_text, parse_mode='HTML')
