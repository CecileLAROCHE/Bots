import os
import discord
import json
import asyncio
import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Charger variables d’environnement
load_dotenv()
TOKEN = os.getenv("TOKEN_DISCORD")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Charger les événements depuis events.json
def load_events():
    with open("events.json", "r") as f:
        return json.load(f)

events = load_events()

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    check_events.start()  # Démarrer la tâche de vérification

# Fonction qui parse la date
def parse_datetime(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")

# Tâche qui vérifie toutes les minutes
@tasks.loop(minutes=1)
async def check_events():
    now = datetime.datetime.now()
    for event in events:
        event_time = parse_datetime(event["time"])
        if (now.year, now.month, now.day, now.hour, now.minute) == \
           (event_time.year, event_time.month, event_time.day, event_time.hour, event_time.minute):

            channel = bot.get_channel(event["channel_id"])
            if channel:
                await channel.send(event["message"])
                print(f"📨 Rappel envoyé pour : {event['name']}")
                update_event_time(event)
            else:
                print(f"❌ Canal introuvable pour : {event['name']}")

# Fonction pour gérer la répétition
def update_event_time(event):
    dt = parse_datetime(event["time"])
    if event["repeat"] == "daily":
        dt += datetime.timedelta(days=1)
    elif event["repeat"] == "weekly":
        dt += datetime.timedelta(weeks=1)
    elif event["repeat"] == "hourly":
        dt += datetime.timedelta(hours=1)
    else:
        return  # pas de répétition

    event["time"] = dt.strftime("%Y-%m-%d %H:%M")
    save_events()

# Sauvegarder les événements mis à jour
def save_events():
    with open("events.json", "w") as f:
        json.dump(events, f, indent=2)

bot.run(TOKEN)

