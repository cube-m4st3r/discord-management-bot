import discord
from discord import app_commands
from discord.ext import commands
import database as db

class FollowMenuButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode

    async def callback(self, interaction: discord.Interaction):
        interaction.response.defer()

class FollowMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FollowMenuButton("Folgen", discord.ButtonStyle.primary, 0))

class user_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_stats", description="Statistiken eines Nutzers anzeigen")
    async def user_stats(self, interaction: discord.Interaction, member: discord.Member=None):

        user_stats_embed = discord.Embed()
        user_stats_embed.color = discord.Color.gold()
        user_stats_embed.set_footer(text=f"requested by: {interaction.user.name}")

        if member:

            student_name = db.select_student_name(str(member.id))
            user_stats_embed.title = str(f"{student_name[0]} {student_name[1]}")

            if db.check_privacy(str(member.id)) == False:
                print(db.check_privacy(str(member.id)))
                await interaction.response.send_message(embed=user_stats_embed)
            else:
                await interaction.response.send_message("User profile is set to private!")
        else:
            student_name = db.select_student_name(str(interaction.user.id))
            user_stats_embed.title = str(f"{student_name[0]} {student_name[1]}")

            if db.check_privacy(str(interaction.user.id)) == False:
                await interaction.response.send_message(embed=user_stats_embed)
            else:
                await interaction.response.send_message(embed=user_stats_embed, ephemeral=True)

        #await interaction.response.send_message(view=user_statsView(interaction))

async def setup(bot):
    await bot.add_cog(user_stats(bot))