import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- Hàm tạo chữ phát sáng (glow) và căn giữa ---
    def draw_glowing_text(self, base, text, font, center_pos,
                          glow_color=(255, 255, 255),
                          text_color=(255, 255, 255)):

        draw = ImageDraw.Draw(base)
        # Tính kích thước chữ để căn giữa
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = center_pos[0] - text_w // 2
        y = center_pos[1] - text_h // 2

        # --- Tạo layer phát sáng ---
        glow_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
        glow_draw = ImageDraw.Draw(glow_layer)

        # Vẽ nhiều lớp mờ để tạo ánh sáng lan toả
        for radius in [10, 8, 6, 4, 2]:
            glow_draw.text((x, y), text, font=font, fill=glow_color)
            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius))

        # Dán layer phát sáng lên nền
        base.alpha_composite(glow_layer)

        # Vẽ chữ thật (nét rõ, có viền)
        draw.text(
            (x, y),
            text,
            font=font,
            fill=text_color,
            stroke_width=3,
            stroke_fill=(0, 0, 0)
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # --- Ảnh nền ---
        bg_path = os.path.join("assets", "greeting.png")
        base = Image.open(bg_path).convert("RGBA")

        # --- Lấy avatar người dùng ---
        avatar_asset = member.display_avatar.replace(size=256)
        avatar_bytes = await avatar_asset.read()
        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")

        # --- Resize & bo tròn avatar ---
        avatar_size = 200
        avatar = avatar.resize((avatar_size, avatar_size))
        mask = Image.new("L", (avatar_size, avatar_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
        avatar.putalpha(mask)

        # --- Dán avatar vào ảnh nền ---
        avatar_x, avatar_y = 1238, 201  # tọa độ avatar (trái trên)
        base.paste(avatar, (avatar_x, avatar_y), avatar)

        # --- Thêm chữ tên người mới ---
        font_path = os.path.join("assets", "iCiel Cucho Bold.otf")
        font_size = 50
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        text = member.global_name or member.display_name

        # Tọa độ này là *tâm chữ*, không phải góc trái
        text_center = (1338, 440)
        self.draw_glowing_text(
            base,
            text,
            font,
            text_center,
            glow_color=(255, 255, 255),
            text_color=(255, 255, 255)
        )

        # --- Xuất ảnh ra buffer ---
        with io.BytesIO() as image_binary:
            base.save(image_binary, "PNG")
            image_binary.seek(0)

            # Gửi vào kênh chào mừng
            channel_id = 1373610717110075392
            channel = member.guild.get_channel(channel_id)
            if channel:
                await channel.send(
                    file=discord.File(fp=image_binary, filename="welcome.png")
                )

# --- Setup cho Cog ---
async def setup(bot):
    await bot.add_cog(Welcome(bot))
