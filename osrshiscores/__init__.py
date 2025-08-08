from .osrs import Runescape


async def setup(bot):
    await bot.add_cog(Runescape(bot))
