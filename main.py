import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ================================
#  .ENV YÜKLE
# ================================
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN .env dosyasında bulunamadı!")

# ================================
#  BOT AYARLARI
# ================================
intents = discord.Intents.default()
intents.message_content = True  # Mesaj içeriklerini okuyabilmesi için

bot = commands.Bot(command_prefix="!", intents=intents)


# ================================
#  HAZIR OLDUĞUNDA
# ================================
@bot.event
async def on_ready():
    print(f"Bot olarak giriş yapıldı: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Game(name="Yapay Zeka Hazırlanıyor...")
    )


# ================================
#  BASİT TEST KOMUTLARI
# ================================
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """Botun çalıştığını test etmek için basit komut."""
    await ctx.send("Pong! 🏓")


@bot.command(name="yardim")
async def yardim(ctx: commands.Context):
    """Kullanılabilir temel komutları gösterir."""
    mesaj = (
        "**🤖 Yapay Zeka Botu (Adım 1 – Temel İskelet)**\n\n"
        "`!ping`  → Botun çalışıp çalışmadığını kontrol eder.\n"
        "`!yardim` → Bu mesajı gösterir.\n\n"
        "Şu an sadece temel iskelet aktif. Bir sonraki adımda yapay zeka eklenecek. "
        "Her yeni sürüm, önceki özellikleri **kaybetmeyecek**."
    )
    await ctx.send(mesaj)


# ================================
#  BOTU BAŞLAT
# ================================
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
