from redbot.core import commands, app_commands
import discord
import aiohttp
from typing import List, Optional

class Runescape(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_url = "http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player="
        self.skill_list = [
            "Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged",
            "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing",
            "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility",
            "Thieving", "Slayer", "Farming", "Runecraft", "Hunter", "Construction"
        ]

    def _commafy(self, num: Optional[str]) -> str:
        try:
            return "{:,}".format(int(num))
        except ValueError:
            return "N/A"

    def _fmt_hs_embed(self, username: str, data: List[str]) -> discord.Embed:
        embed = discord.Embed(
            title=f"OSRS Highscores for {username.replace('_', ' ')}",
            color=discord.Color.from_rgb(255, 215, 0)
        )

        for i, skill in enumerate(self.skill_list):
            if i >= len(data):
                embed.add_field(name=skill, value="No data", inline=True)
                continue

            splitted = data[i].split(',')
            if len(splitted) == 3:
                rank, level, xp = map(self._commafy, splitted)

                embed.add_field(
                    name=skill,
                    value=f"**Level:** {level}\n**XP:** {xp}\n**Rank:** {rank}",
                    inline=True
                )
            else:
                embed.add_field(name=skill, value="No data", inline=True)

        embed.set_footer(text="Old School RuneScape Highscores | Data retrieved in real-time")
        return embed

    @app_commands.command(name="hs", description="Show OSRS highscores for a given username.")
    @app_commands.describe(username="OSRS username to look up")
    async def hs(self, interaction: discord.Interaction, username: str):
        username = username.replace(" ", "_")
        url = self.base_url + username

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await interaction.response.send_message(f"Error: Received status code {response.status}.", ephemeral=True)
                        return

                    raw_text = await response.text()
                    lines = raw_text.replace("\r", "").split("\n")
                    data = [line for line in lines if line.strip() and len(line.split(',')) == 3]
                    data = data[:len(self.skill_list)]
        except aiohttp.ClientError as e:
            print("Network error fetching data from API:", e)
            await interaction.response.send_message("A network error occurred. Please try again later.", ephemeral=True)
            return
        except Exception as e:
            print("Error fetching data from API:", e)
            await interaction.response.send_message("An unexpected error occurred. Please try again.", ephemeral=True)
            return

        if not data:
            await interaction.response.send_message("No hiscore data found for this username.", ephemeral=True)
            return

        embed = self._fmt_hs_embed(username, data)
        await interaction.response.send_message(embed=embed)
