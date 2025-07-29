import os
import sys
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Debug : afficher le répertoire de travail et son contenu
cwd = os.getcwd()
print(f"📂 Working directory: {cwd}")
print("📑 Contenu du dossier :", os.listdir(cwd))

# 1) Charger .env (préciser le chemin explicite)
env_path = os.path.join(cwd, ".env")
print(f"🔍 Recherche de {env_path} → exists? {os.path.exists(env_path)}")
load_dotenv(dotenv_path=env_path)

# 2) Récupérer le token
token = os.getenv("TOKEN_DISCORD")
if not token:
    print("❌ ERREUR : la variable TOKEN_DISCORD n'est pas définie dans .env")
    sys.exit(1)

print(f"🔐 Token lu : {token[:10]}...")  # n'affiche que les 10 premiers caractères

# 3) Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong ! 🏓")

# 4) Lancer le bot
bot.run(token)