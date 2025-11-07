import os
import sys
import types
if 'audioop' not in sys.modules:
    audioop = types.ModuleType('audioop')
    # mock các hàm chính, trả về dummy
    audioop.add = lambda a, b: 0
    audioop.max = lambda a, b: 0
    audioop.minmax = lambda a, b: (0,0)
    sys.modules['audioop'] = audioop
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread


# --- Load biến môi trường ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise SystemExit("❌ Không tìm thấy DISCORD_TOKEN trong file .env!")

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # cần cho event on_member_join

# --- Bot setup ---
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Flask keep-alive ---
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Drunken Raccoon bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()

# --- Khi bot sẵn sàng ---
@bot.event
async def on_ready():
    print(f"✅ Đăng nhập thành công: {bot.user}")
    print("🔄 Đang đồng bộ slash commands...")
    try:
        synced = await bot.tree.sync()
        print(f"✨ Đã đồng bộ {len(synced)} slash command(s)")
    except Exception as e:
        print(f"⚠️ Lỗi khi sync: {e}")

# --- Tự động load cogs ---
@bot.event
async def setup_hook():
    cogs_dir = "./cogs"
    if not os.path.exists(cogs_dir):
        print("⚠️ Không tìm thấy thư mục cogs!")
        return

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"📦 Loaded module: {filename}")
            except Exception as e:
                print(f"⚠️ Lỗi khi load {filename}: {e}")

# --- Chạy bot ---
if __name__ == "__main__":
    keep_alive()  # giữ bot online bằng Flask (Render + UptimeRobot)
    bot.run(TOKEN)
