import os
import sys
import types

# fix audioop (Render python 3.13)
if 'audioop' not in sys.modules:
    audioop = types.ModuleType('audioop')
    audioop.add = lambda a, b: 0
    audioop.max = lambda a, b: 0
    audioop.minmax = lambda a, b: (0,0)
    sys.modules['audioop'] = audioop

import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

# ===== LOAD ENV =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise SystemExit("❌ Không tìm thấy DISCORD_TOKEN")

# ===== DISCORD =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== FLASK =====
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is alive"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def setup_hook():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded {file}")

# ===== MAIN =====
if __name__ == "__main__":
    print("🚀 Starting Flask + Discord bot")

    threading.Thread(target=run_flask).start()

    bot.run(TOKEN)
