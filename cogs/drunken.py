import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime
import os

class SmallTalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_message = None
        self.talk_loop.start()  # Bắt đầu loop khi cog load

    def cog_unload(self):
        self.talk_loop.cancel()

    async def send_random_message(self):
        """Hàm gửi message random vào channel"""
        try:
            channel_id = int(os.getenv("CHAT_CHANNEL_ID", "0"))
        except ValueError:
            channel_id = 0

        if channel_id == 0:
            print("⚠️ Không có CHAT_CHANNEL_ID trong .env hoặc ID không hợp lệ.")
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(f"⚠️ Không tìm thấy channel ID {channel_id}")
            return

        messages = [
            "Bình rượu lão phu mới để đây đâu mất rồi? Kẻ nào dám giấu rượu của lão phu? 🤨",
            "Nay có gì vui không mấy đứa?",
            "Dậy đi mấy đứa, bữa nay cày cuốc gì chưa?",
            "Ta chưa say.....chỉ hơi xoay xoay thôi 😵",
            "Ai rót cho ta thêm ly nữa nào.",
            "Bảo Bảo nha đầu ngốc, mấy hôm nay ngươi không dắt mọi người đi nhảy quảng trường nữa à? 🥴 Lão phu muốn thấy tên Hổ tiểu tử đó lắc mông giữa tông môn. Cười chết lão phu rồi. 🤣",
            "Bảo Bảo, nếu tên Khanh Khanh kia bắt nạt ngươi, cứ việc nói với lão phu. Để lão phu cho hắn một bài học. 😡",
            "Ủa.....ai lấy mất bình rượu của ta nữa rồi? 🤬",
            "Tụi bây ngủ hết chưa? Chán quá nè.",
            "Tiểu tử kia, làm hết nhiệm vụ ngày hôm nay chưa?",
            "Không ai thèm ngó ngàng gì tới lão thần thú này hết 😤",
            "Ai đó đi bảo tên Hổ tiểu tử mang rượu lên cho ta.",
            "Tiểu Lạc, đi bảo trù phòng ngày hôm nay lão Hùng ta muốn ăn linh mễ và gà nướng ngũ vị. 🍗🧄🧅🫚🌿🌶️",
            "Tiểu Lạc, đi bảo trù phòng ngày hôm nay lão Hùng ta muốn ăn thịt heo nướng mật ong. 🍖🍯",
            "Tiểu Lạc, đi bảo trù phòng ngày hôm nay lão Hùng ta muốn ăn mì. 🍜",
            "Tiểu Lạc, đến trù phòng lấy chút đồ ngọt cho lão phu 🥧🍮🍩🥯🥞 Yên tâm, không thiếu chỗ tốt cho ngươi.",
            "Ai đó đi tìm Sầu Riêng giúp lão phu, nha đầu ngốc đó lại lủi thủi đi nghe nhạc một mình rồi.",
            "Này Cá nha đầu! Đừng trêu chọc sư phụ ngươi nữa, hắn có tuổi rồi, ngươi không sợ hắn đau tim xong vũ hóa phi thăng sao? 🥲",
            "Ai đó nhắc tên Dao tiểu tử nhớ đi làm nhiệm vụ với nha đầu Sứa đi. Tên đó lười lắm, nếu không ai nhắc hắn sẽ không làm đâu. 🫩",
            "Này tiểu Diệp, sao hôm nay ngươi không đi cùng tiểu Giản?",
            "Này tiểu Giản, tiểu Diệp đâu rồi?",
            "Ô là Mèo Măng đấy à? Nha đầu ngươi đã cơm nước gì chưa?",
            "Các ngươi nhớ nhắc tên Dao tiểu tử tu luyện cho đàng hoàng, đúng là làm cho lão phu thao nát tâm mà. 😩",
            "Gấu tiểu tử là cháu ruột của lão phu! Các ngươi không được bắt nạt hắn, biết chưa? 😎",
            "Tiểu tử Mèo Mun mấy nay tu luyện như nào rồi? Không được lơ là đâu biết chưa? 🧐",
            "Tiểu Diệp với tiểu Giản lại đi đâu đấy?",
            "Lão tổ mà có hỏi, thì các người bảo không có gặp qua ta, nhớ chưa? 😨",
            "Một thời tung hoành ngang dọc, hùng cứ một phương, mà giờ lại phải ngồi đây trông chừng đám tiểu bối các ngươi. Chán chết lão Hùng ta rồi."
        ]

        # Tránh gửi 2 tin nhắn giống nhau liên tiếp
        choices = [m for m in messages if m != self.last_message]
        msg = random.choice(choices)
        self.last_message = msg

        await channel.send(msg)
        print(f"✅ Sent smalltalk: {msg}")

    @tasks.loop(count=1)  # Loop chạy 1 lần, sau đó tự gọi lại trong hàm
    async def talk_loop(self):
        await self.bot.wait_until_ready()

        now = datetime.datetime.now()
        # Random giờ, phút, giây trong ngày
        target_time = datetime.datetime.combine(
            now.date(),
            datetime.time(
                random.randint(0, 23),
                random.randint(0, 59),
                random.randint(0, 59)
            )
        )
        if target_time < now:
            target_time += datetime.timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        print(f"🕓 SmallTalk tiếp theo vào {target_time.strftime('%H:%M:%S')} ({wait_seconds/3600:.1f} giờ nữa)")

        # Chờ tới thời điểm random
        await asyncio.sleep(wait_seconds)
        await self.send_random_message()

        # Sau khi gửi xong → gọi lại chính loop này để tạo giờ mới ngày hôm sau
        self.talk_loop.restart()

    @talk_loop.before_loop
    async def before_talk_loop(self):
        await self.bot.wait_until_ready()

    # --- Lệnh test gửi ngay lập tức ---
    @commands.command(name="wheremybottle")
    async def wheremybottle(self, ctx):
        await self.send_random_message()

async def setup(bot):
    await bot.add_cog(SmallTalk(bot))
