import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from ai.ai_core import ask_ai

# ================================
#  .ENV YÜKLEME
# ================================
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN .env dosyasında bulunamadı!")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY .env dosyasında bulunamadı!")


# ================================
#  CLIENT & SLASH TREE OLUŞTURMA
# ================================
class BotClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        # Slash komut ağacı
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Bot giriş yaptı: {self.user} (ID: {self.user.id})")

        # Slash komutlarını senkronize et
        try:
            synced = await self.tree.sync()
            print(f"[Slash] {len(synced)} komut senkronize edildi.")
        except Exception as e:
            print(f"[Slash] Sync hatası: {e}")

        await self.change_presence(
            activity=discord.Game(name="/ai komutu aktif!")
        )


client = BotClient()
tree = client.tree


# ================================
#  /ping — SLASH TEST KOMUTU
# ================================
@tree.command(name="ping", description="Botun çalışıp çalışmadığını gösterir.")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")


# ================================
#  /yardim — HELP KOMUTU
# ================================
@tree.command(name="yardim", description="Kullanılabilir tüm komutları gösterir.")
async def slash_yardim(interaction: discord.Interaction):
    mesaj = (
        "**🤖 Yapay Zeka Botu – Sadece Slash Sistemi Aktif**\n\n"
        "Kullanılabilir komutlar:\n"
        "• **/ping** → Bot testi\n"
        "• **/yardim** → Yardım menüsü\n"
        "• **/ai** → Yapay zeka ile konuşma\n\n"
        "Bir sonraki adımda role/kanal izinleri eklenecek."
    )
    await interaction.response.send_message(mesaj)


# ================================
#  /ai — YAPAY ZEKA KOMUTU
# ================================
@tree.command(name="ai", description="Yapay zeka ile sohbet et.")
async def slash_ai(interaction: discord.Interaction, mesaj: str):
    await interaction.response.defer()  # typing göstermek için

    cevap = ask_ai(mesaj)

    if len(cevap) > 1900:
        cevap = cevap[:1900] + "\n...\n⚠️ Mesaj uzun olduğu için kısaltıldı."

    await interaction.followup.send(cevap)


# ================================
#  BOTU BAŞLAT
# ================================
client.run(DISCORD_TOKEN)
