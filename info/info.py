import discord
from redbot.core import commands, app_commands
import aiohttp
from io import BytesIO
from PIL import Image

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Show a user's profile picture and account info.")
    @app_commands.describe(user="The user to look up. Defaults to you.")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user

        avatar_url = user.display_avatar.replace(format='png', size=128).url
        color = discord.Color.blurple()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url) as resp:
                    if resp.status == 200:
                        image_bytes = await resp.read()
                        img = Image.open(BytesIO(image_bytes)).convert("RGB")
                        pixels = list(img.getdata())
                        median = tuple(sorted(pixels)[len(pixels) // 2])
                        color = discord.Color.from_rgb(*median)
        except Exception as e:
            print(f"Failed to extract avatar color: {e}")

        created_at = user.created_at.strftime("%B %d, %Y")
        joined_at = user.joined_at.strftime("%B %d, %Y") if user.joined_at else "Unknown"

        embed = discord.Embed(
            title=f"{user.name}'s account info",
            color=color
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Account Created", value=created_at, inline=True)
        embed.add_field(name="Joined Server", value=joined_at, inline=True)

        await interaction.response.send_message(embed=embed)
