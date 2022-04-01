import datetime
import discord

from discord.ext import commands
from discord.ext.commands import bot_has_permissions
from discord import Embed, Interaction, SelectOption, slash_command

from utils.utils import all_commands
from utils.color import Color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Dropdown(discord.ui.Select):
    def __init__(self):
        self.command_list = [SelectOption(label=command[0], description=command[1]['description']) for command in all_commands.items()]
        self.command_list.append(
            SelectOption(label="All commands", description="Get help about all the commands")
            )
        super().__init__(
            placeholder="Choose a command.",
            min_values=1,
            max_values=1,
            options=self.command_list,
        )

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Help", 
            description=f"**Get some help about __{self.values[0].casefold()}__**", 
            color=Color.get_color("lite"),
            timestamp=datetime.datetime.utcnow())
        if self.values[0] != "All commands":
            embed.add_field(name="Description", value=all_commands[self.values[0]]['description'])
            embed.add_field(name="Utilisation", value=f"``{all_commands[self.values[0]]['utilisation']}``")
        else:
            for command in all_commands.items():
                embed.add_field(
                    inline=False, 
                    name=command[0].capitalize(), 
                    value=f"{(command[1]['description'])}\n``{command[1]['utilisation']}``"
                    )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())

class Help_command(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @bot_has_permissions(send_messages=True, read_messages=True)
    @slash_command(name="help", description="Get some help about commands", guild_ids=guilds)
    async def help(self, ctx: Interaction):
        view = DropdownView()

        embed = Embed(title="Help", description=f"Get some help about commands", color=Color.get_color("lite"), timestamp=datetime.datetime.utcnow())
        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)

        log = {
            "action": "help", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}}
            
        logger.info(log)

def setup(bot):
    bot.add_cog(Help_command(bot))
