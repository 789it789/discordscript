from discord.ext import commands
import aiohttp
from cogs.utils.chat_formatting import *
import fractions

try:
    import feedparser
except:
    feedparser = None


class Runescape:

    def __init__(self, bot):
        self.bot = bot
        self.base_url = \
            "http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player="
        self.max_level = 99
        self.skill_list = [
            "Overall",
            "Attack",
            "Defence",
            "Strength",
            "Constitution",
            "Ranged",
            "Prayer",
            "Magic",
            "Cooking",
            "Woodcutting",
            "Fletching",
            "Fishing",
            "Firemaking",
            "Crafting",
            "Smithing",
            "Mining",
            "Herblore",
            "Agility",
            "Thieving",
            "Slayer",
            "Farming",
            "Runecrafting",
            "Hunter",
            "Construction",
        ]
        self.elite_skills = [23, ]
        self.skill_levels = self._skill_levels()
        self.elite_levels = [0.4796 * pow(x, 4) - 12.788 * pow(x, 3) + 228.56 *
                             pow(x, 2) + 2790.8 * x - 31674
                             for x in range(1, 150)]

    def _skill_levels(self):
        xplist = []

        points = 0
        for level in range(1, self.max_level):
            points += int(level + 300 * pow(2, level / 7))
            xplist.append(int(points / 4))

        return xplist

    def _get_level(self, exp):
        exp = int(exp)
        for level, currExp in enumerate(self.skill_levels):
            if currExp > exp:
                return str(level + 1)
        return '120'

    def _get_elite_level(self, exp):
        exp = int(exp)
        for level, currExp in enumerate(self.elite_levels):
            if currExp > exp:
                return str(level + 1)
        return '150'

    def _commafy(self, num):
        try:
            int(num)
        except:
            return num
        else:
            return "{:,}".format(int(num))

    def _fmt_hs(self, data):
        ret = "```"
        retlist = [['Skill', 'Rank', 'Level', 'Experience']]
        for i in range(len(data)):
            if i < len(self.skill_list):
                splitted = data[i].split(',')
                if i != 0:
                    if i in self.elite_skills:
                        splitted[1] = self._get_elite_level(splitted[2])
                    else:
                        splitted[1] = self._get_level(splitted[2])
                splitted[0] = self._commafy(splitted[0])
                splitted[1] = self._commafy(splitted[1])
                splitted[2] = self._commafy(splitted[2])
                retlist.append([self.skill_list[i]] + splitted)
        col_width = max(len(word) for row in retlist for word in row) + 2
        for row in retlist:
            ret += "".join(word.ljust(col_width) for word in row) + "\n"
        ret += "```"
        return ret

    @commands.command(no_pm=True)
    async def hs(self, *, username):
        """Gets hiscores info"""
        username = username.replace(" ", "_")
        url = self.base_url + username
        try:
            page = await aiohttp.get(url)
            text = await page.text()
            text = text.replace("\r", "")
            text = text.split("\n")
        except:
            await self.bot.say("No user found.")
        else:
            await self.bot.say(self._fmt_hs(text))

def setup(bot):
    n = Runescape(bot)
bot.add_cog(n)