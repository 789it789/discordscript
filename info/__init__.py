from .info import UserInfo


async def setup(bot):
    await bot.add_cog(UserInfo(bot))
