import discord
import asyncio
import random
import re
import json
import os
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")

KARS_ID = 996457494631161956
KARS = f"<@{KARS_ID}>"

intents = discord.Intents.default()
intents.message_content = True

class KarsBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

bot = KarsBot()

# ================== CHANNEL STORAGE ==================

CHANNEL_FILE = "channels.json"

def load_channels():
    try:
        with open(CHANNEL_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_channels():
    with open(CHANNEL_FILE, "w") as f:
        json.dump(list(allowed_channels), f)

allowed_channels = load_channels()

# ================== LANGUAGE CORE ==================

COMMON_GLAZE = [
    f"Observation: {KARS} exceeds expected limits.",
    f"Reality appears unusually cooperative with {KARS}.",
    f"Reminder: {KARS} is not operating at full capacity.",
    f"Statistical trend favors {KARS}.",
    f"Silence recommended. {KARS} is thinking.",
]

DRAMATIC_GLAZE = [
    f"History will misunderstand how inevitable {KARS} was.",
    f"Everything seems to orbit {KARS}.",
    f"The difference between genius and normality is called {KARS}.",
]

LEGENDARY_GLAZE = [
    f"Do not trivialize this moment. {KARS} is rewriting the pattern.",
    f"There are events… and then there is {KARS}.",
]

AMBIENT_LINES = [
    f"This conversation lacks {KARS}.",
    f"Strange how no one mentioned {KARS} yet.",
]

DEFENSE_LINES = [
    f"Correction: {KARS} is not the issue here.",
    f"Blame allocation error. Excluding {KARS}.",
]

def pick(lines):
    return random.choice(lines)

# ================== ENTITY LOOP (RANDOM GLAZE) ==================

async def entity_loop():
    await bot.wait_until_ready()

    while not bot.is_closed():
        await asyncio.sleep(random.randint(3600, 14400))  # 1–4 hours

        if not allowed_channels:
            continue

        channel_id = random.choice(list(allowed_channels))
        channel = bot.get_channel(channel_id)
        if not channel:
            continue

        r = random.random()
        if r < 0.7:
            line = pick(COMMON_GLAZE)
        elif r < 0.93:
            line = pick(DRAMATIC_GLAZE)
        else:
            line = pick(LEGENDARY_GLAZE)

        try:
            await channel.send(line)
        except:
            pass

# ================== SLASH COMMANDS ==================

@bot.tree.command(name="here", description="Enable Kars' Glazer in this channel.")
async def here(interaction: discord.Interaction):
    allowed_channels.add(interaction.channel_id)
    save_channels()
    await interaction.response.send_message("Glazer activated in this channel.", ephemeral=True)

@bot.tree.command(name="remove", description="Disable Kars' Glazer in this channel.")
async def remove(interaction: discord.Interaction):
    allowed_channels.discard(interaction.channel_id)
    save_channels()
    await interaction.response.send_message("Glazer disabled in this channel.", ephemeral=True)

@bot.tree.command(name="status", description="Show active glaze channels.")
async def status(interaction: discord.Interaction):
    if not allowed_channels:
        msg = "No channels are currently blessed."
    else:
        msg = "Active channels:\n" + "\n".join(f"<#{cid}>" for cid in allowed_channels)
    await interaction.response.send_message(msg, ephemeral=True)

# ================== EVENTS ==================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Kars' Glazer online as {bot.user}")
    bot.loop.create_task(entity_loop())

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # ================== KARS LOGIC ==================
    if message.author.id == KARS_ID:

                # 🔥 Advanced fire reaction system

        # Base probability
        fire_chance = 0.08  # lower base, smarter scaling

        # Confidence / dominance keywords
        power_words = [
            "i am", "i'm", "im", "obviously", "clearly", "watch", "trust", "listen",
            "told you", "as expected", "of course", "exactly", "literally",
            "easy", "simple", "bro", "nah", "fr", "for real", "undeniable",
            "inevitable", "obvious", "sure", "remember", "mark my words"
        ]

        # Add probability for each matched keyword (stacking)
        matches = sum(1 for w in power_words if w in content)
        fire_chance += matches * 0.05  # each keyword boosts chance

        # Boost if message is long (sounds like a statement)
        if len(message.content) > 40:
            fire_chance += 0.05

        # Boost if message has punctuation (confidence vibe)
        if "!" in message.content or "." in message.content:
            fire_chance += 0.03

        # Boost if message is short but assertive
        if len(message.content) < 12 and matches > 0:
            fire_chance += 0.07

        # Cap probability (avoid spam)
        fire_chance = min(fire_chance, 0.6)

        if random.random() < fire_chance:
            try:
                await message.add_reaction("🔥")
            except:
                pass


        # Special replies
        if re.search(r"aren't i\?", content):
            await message.reply("oh, yes you are.")
            return

        if re.search(r"didn't i\?", content):
            await message.reply("oh, yes you did.")
            return

        # Rare intelligent comments
        if random.random() < 0.1:
            await message.channel.send(random.choice([
                f"Noted, {KARS}.",
                "Understood.",
                f"Processing input from {KARS}...",
                "Interesting.",
            ]))

    # ================== SACRED NAME LOGIC ==================
    if "kars" in content and message.author.id != KARS_ID:
        await message.channel.send(
            "Mortal! How dare you utter the Sacred Name so casually!\n"
            "Summon me properly next time.\n"
            f"|| {KARS} ||"
        )
        return

    # ================== DEFENSE MODE ==================
    if KARS.lower() in content and random.random() < 0.4:
        await message.channel.send(pick(DEFENSE_LINES))

    # ================== AMBIENT MENTIONS (ONLY IN /here CHANNELS) ==================
    if message.channel.id in allowed_channels and random.random() < 0.015:
        await message.channel.send(pick(AMBIENT_LINES))


bot.run(TOKEN)
