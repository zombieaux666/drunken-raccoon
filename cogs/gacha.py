import discord
from discord.ext import commands
import random
import os

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.allowed_channel = int(os.getenv("GACHA_CHANNEL_ID", "0"))
        except ValueError:
            self.allowed_channel = 0

    @commands.command(name="gacha")
    async def gacha(self, ctx, *, items: str=""):
        """
        !gacha item1, item2, item3
        Bot sẽ chọn ngẫu nhiên 1 item trong danh sách,
        chỉ trong channel được phép, kèm phản hồi ngẫu nhiên.
        """
        if self.allowed_channel == 0:
            await ctx.send("⚠️ Gacha chưa được cấu hình channel.")
            return

        if ctx.channel.id != self.allowed_channel:
            await ctx.send(f"Tiểu tử kia, muốn gacha thì xuống dưới <#{self.allowed_channel}> nha!")
            return

        # Tách chuỗi theo dấu phẩy, bỏ khoảng trắng thừa
        item_list = [i.strip() for i in items.split(",") if i.strip()]
        if not item_list:
            await ctx.send("Ngươi bảo ta chọn gì cơ? Có cái gì đâu mà chọn!")
            return
        

        # Random kết quả
        choice = random.choice(item_list)

        # Danh sách phản hồi vui nhộn
        responses = [
            f"**{choice}** đi chứ gì nữa.",
            f"Tầm này không gì qua được **{choice}**.",
            f"Thích **{choice}** đúng không? Chứ mấy cái kia nghe như thêm cho đủ số.",
            f"Nghe người đi trước, **{choice}** là tốt nhất.",
            f"**{choice}** là lựa chọn tốt nhất cho trẻ sơ sinh và trẻ nhỏ.",
            f"***{choice}!!!*** ***{choice}!!!*** ***{choice}!!!***",
            f"Một nhà hiền triết đã từng nói: ***\"{choice}\"***.",
            f"**{choice}**, lựa chọn hàng đầu của mọi nhà.",
            f"Dân chơi là phải chọn **{choice}**.",
            f"**{choice}** là chân ái!!!",
            f"*Mỹ nhân trong thiên hạ đều tầm thường đối với ta, chỉ có **{choice}** mới làm ta hứng thú!*",
            f"Ta nghe lão tổ từng nói, ***{choice}*** là bí quyết để trường sinh bất lão.",
            f"*Ta thà phụ thiên hạ, chứ không thể không chọn **{choice}**.*",
            f"Thà là không chọn, chứ đã chọn thì phải là **{choice}**.",
        ]

        msg = random.choice(responses)
        await ctx.send(f"{msg}")

# --- Setup cho Cog ---
async def setup(bot):
    await bot.add_cog(Gacha(bot))
