import discord
import db


class UnregisteredButton(discord.ui.Button):
    def __init__(self, text, style, mode, user):
        super().__init__(label=text, style=style, disabled=False)
        self.__user = user
        self.__mode = mode

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.__user.id:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        match self.__mode:
            case "register":
                await interaction.response.send_modal(RegisterModal(db.get_user_with_id(self.__user.id)))
            case "cancel":
                return


class RegisterModal(discord.ui.Modal):
    def __init__(self, user):
        super().__init__(title="Registriere dich hier!")
        self.__user = user

        self.__first_name = discord.ui.TextInput(label="Vorname", placeholder="Bitte trage hier deinen Vornamen ein.", required=True)
        self.__last_name = discord.ui.TextInput(label="Nachname", placeholder="Bitte trage hier deinen Nachnamen ein.", required=True)
        self.__address = discord.ui.TextInput(label="Addresse (freiwillig)", placeholder="Bitte trage hier Straße, Hausnummer, PLZ ein.", required=True)
        self.__email = discord.ui.TextInput(label="E-Mail (freiwillig)", placeholder="Bitte trage hier deine E-Mail ein.", required=True)

        self.add_item(self.__first_name)
        self.add_item(self.__last_name)
        self.add_item(self.__address)
        self.add_item(self.__email)

    async def on_submit(self, interaction: discord.Interaction):



