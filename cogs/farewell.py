import discord
from discord.ext import commands
import os

class Farewell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.channel_id = int(os.getenv("FAREWELL_CHANNEL_ID", "0"))
        except ValueError:
            self.channel_id = 0

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if self.channel_id == 0:
            return

        channel = member.guild.get_channel(self.channel_id)
        if not channel:
            return

        # Lấy tên hiển thị (global_name hoặc username)
        display_name = member.global_name or member.name

        # Thông báo: mention member + hiển thị global_name
        # Khi mention, Discord sẽ highlight tên của user
        message = f"Đạo hữu {member.mention} ({member.display_name}) đã hình thần câu diệt!!!~~~"

        await channel.send(message)

# --- Setup Cog ---
async def setup(bot):
    await bot.add_cog(Farewell(bot))
