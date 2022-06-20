import re
from discord.ext import commands
import database

class karma(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

        has_karma_modifier = re.match('<@\d+>.*(\+{2}|\-{2})', message.content)

        if has_karma_modifier is not None:
            user = re.search('<@(\d+)>', message.content).group(1)

            operation = re.search('(\+{2}|\-{2})', message.content).group()

            result = database.update_user_karma(user, operation)
            await message.channel.send(f'<@{user}> new karma is now {result}')

        has_user_modifier = re.match('@(\d+|\w+).*(\+{2}|\-{2})', message.content)

        if has_user_modifier is not None and has_karma_modifier is None:
            user = re.search('(\d+|\w+)', message.content).group(1)

            if self.is_user_in_server(user, message.guild) == False:
                operation = '--'
                result = database.update_user_karma(message.author.id, operation)
                await message.channel.send(f'User {user} not found in this server. Negative RiGCz reward deployed. <@{message.author.id}> new karma is {result}')


    def is_user_in_server(self, user_id, guild):
        for user in guild.members:
            if user_id == user.id:
                return True

        return False