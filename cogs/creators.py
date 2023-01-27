import discord
from discord import app_commands
from discord.ext import commands
from util import accessutils


# Modal for class creation
class classCreation(discord.ui.Modal, title='DC Class Creator'):
    classname = discord.ui.TextInput(label='Class Name', style=discord.TextStyle.short)
    classhealth = discord.ui.TextInput(label='Class Health', style=discord.TextStyle.short)
    classdamage = discord.ui.TextInput(label='Class Damage', style=discord.TextStyle.short)
    classdefense = discord.ui.TextInput(label='Class Defense', style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{interaction.user.mention}, you submitted: Class name: {self.classname} '
                                                f'Class Health: {self.classhealth} Class Damage: {self.classdamage} '
                                                f'Class Defense: {self.classdefense}', ephemeral=True)


class creators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Class Creation command
    @app_commands.command(name="createclass", description="Bot owner command to make classes")
    @app_commands.guilds(discord.Object(id=904120920862519396))
    @app_commands.checks.has_permissions(administrator=True)
    async def createclass(self, interaction: discord.Interaction):
        if str(interaction.user.id) in await accessutils.whohasaccess():
            await interaction.response.send_modal(classCreation())
        else:
            await interaction.response.send_message(content=f"You can't run this command", ephemeral=True)


# Required setup function for cog.
async def setup(bot):
    await bot.add_cog(creators(bot))
