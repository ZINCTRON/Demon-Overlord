import discord

class Interaction:
    
    def __init__(self, bot: discord.Client, action: dict, author: str, target: list):
        self.action = action

        if len(target) > 0:
            if author == target[0]:
                self.response = f'{author} {action["action"]} themselves'
            elif len(target) > 1:
                self.response = f'{author} {action["action"]} {", ".join(target[:-1])} and {target[-1]}'
            else:
                self.response = f'{author} {action["action"]} {target[0]}'

            self.embed = discord.Embed(colour=0xff00e7, title=self.response)
    
    async def handler(self, bot:discord.Client) -> discord.Embed:
        self.embed.set_image(url=await bot.tenor.get_interact(f'anime {self.action["name"]}'))
        return self.embed


class AloneInteraction(Interaction):
    def __init__(self, bot: discord.Client, action: dict, author: str):
        Interaction.__init__(self, bot, action, author, [])

        # generate response
        self.response = f'{author} {action["action"]}'
        self.embed = discord.Embed(colour=0xff00e7, title=self.response)


class SocialInteraction(Interaction):
    def __init__(self, bot: discord.Client, action: dict, author: str, target: list):
        Interaction.__init__(self, bot, action, author, target)

    
async def interactions_handler(bot:discord.Client, message:discord.Message, command:list, devRole:discord.Role) -> None:
    

    try:
        action = bot.interactions[command[0]]
        author = message.author.display_name
        mentions = [x.display_name for x in message.mentions]
        if action["type"] == "social":
        
            if len(message.mentions) == 0 and command[2] == "everyone":
                interaction = SocialInteraction(bot, action, author, ["everyone"])
            elif len(message.mentions) > 0:
                interaction = SocialInteraction(bot, action, author, mentions)

        elif action["type"] == "alone":
            interaction = AloneInteraction(bot, action, author)
        await message.channel.send(embed=await interaction.handler(bot))
    # okay... i'm sick of all these errors...
    except Exception as e:
       await message.channel.send(f"**{bot.izzymojis['izzyangry']} INTERACTIONS - ERROR **\nHey {devRole.mention} There was an error.\n```\n{e}\n```")