import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
import threading

load_dotenv()

TOKEN = os.getenv("TOKEN")
# Botun girmesini istediğiniz ses kanalının ID'sini buraya yazın
VOICE_CHANNEL_ID = 1519341566282698903  # <--- Burayı kendi kanal ID'niz ile değiştirin

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Render Port Hatasını Çözmek İçin Web Sunucusu
app = Flask('')

@app.route('/')
def home():
    return "Ses botu aktif ve calisiyor!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")
    
    # Belirttiğiniz ses kanalını buluyoruz
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    
    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            # Ses kanalına bağlanma komutu
            await channel.connect()
            print(f"Başarıyla '{channel.name}' ses kanalına bağlanıldı.")
        except Exception as e:
            print(f"Ses kanalına bağlanırken hata oluştu: {e}")
    else:
        print("Geçersiz kanal ID'si veya kanal bir ses kanalı değil!")

if __name__ == "__main__":
    # Web sunucusunu arka planda başlatıyoruz
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.run(TOKEN)