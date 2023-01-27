import discord
from discord import app_commands
from discord.ext import commands


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sell", description="This is a new test command!")
    async def sell(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Test", ephemeral=True)


async def setup(bot):
    await bot.add_cog(economy(bot))
