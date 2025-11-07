import discord
from discord.ext import commands
import random
import os

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_reply = None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Bỏ qua tin nhắn của bot
        if message.author.bot:
            return

        # Nếu bot bị mention
        if self.bot.user in message.mentions:
            # Danh sách câu reply ngẫu nhiên
            responses = [
                "Kêu gì mà kêu? Ngươi tìm lão phu có việc gì?",
                "Gì cơ? Có rượu miễn phí à? Ở đâu? 🤤",
                "Lão tổ kiếm ta á? Nói với hắn ta đang bế tử quan, nếu chưa đột phá tuyệt không ra ngoài.",
                "Trừ khi ngươi có rượu, không thì đừng làm phiền ta!",
                "Ta nói tên tiểu bối này, tên ta không phải để ngươi gọi loạn đâu 😠",
                "Một con gà nướng, lão Hùng ta có thể bỏ qua cho ngươi lần này.",
                "Ngươi mà là đệ tử ta thì ta đã chụp chết ngươi trên tường rồi đấy 😒",
                "Mỗi một vò rượu mà muốn đổi trúc cơ đan từ ta? NGƯỜI SI NÓI MỘNG!!! Hai vò thì ta xem xét 🤨",
                "Bảo với tên Hổ tiểu tử, nếu còn có người làm phiền ta, thì ta sẽ chụp chết hắn 😡",
                "Láo toét, tên của hộ tông thần thú ta đây là thứ mà một tên tiểu bối như ngươi có thể gọi à? 😤",
                "Ta đang ngủ, trừ khi tông môn bị tập kích, còn không thì đừng kêu ta dậy 💤💤💤",
                "Gì??? Ai??? Kẻ nào!!! Dám xâm phạm Thiên Tiếu??? Đã lâu rồi hồ lô rượu của lão phu chưa thấy máu đây!!!"
            ]
            choices = [r for r in responses if r != self.last_reply]
            reply = random.choice(choices)
            self.last_reply = reply
            await message.channel.send(reply)

# --- Setup cho Cog ---
async def setup(bot):
    await bot.add_cog(Reply(bot))
