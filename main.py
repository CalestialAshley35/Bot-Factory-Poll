import discord
from discord.ext import commands

# Prompt the user to enter their bot token
TOKEN = input("Please enter your Discord bot token: ")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command(name='createpoll')
async def create_poll(ctx, question: str, *options: str):
    if len(options) < 2:
        await ctx.send('A poll must have at least two options.')
        return
    if len(options) > 10:
        await ctx.send('A poll can have a maximum of 10 options.')
        return

    embed = discord.Embed(title="Poll", description=question, color=0x00ff00)
    fields = {chr(0x1F1E6 + i): option for i, option in enumerate(options)}
    for emoji, option in fields.items():
        embed.add_field(name=emoji, value=option, inline=False)

    message = await ctx.send(embed=embed)
    for emoji in fields.keys():
        await message.add_reaction(emoji)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message
    if message.author != bot.user:
        return

    embed = message.embeds[0]
    if embed.title != "Poll":
        return

    poll_fields = [field.name for field in embed.fields]
    if reaction.emoji in poll_fields:
        poll_results = {}
        for emoji in poll_fields:
            poll_results[emoji] = 0

        for reaction in message.reactions:
            if reaction.emoji in poll_fields:
                poll_results[reaction.emoji] += reaction.count - 1  # Exclude the bot's own reaction

        result_description = "\n".join([f"{emoji}: {count}" for emoji, count in poll_results.items()])
        result_embed = discord.Embed(title="Poll Results", description=result_description, color=0xff0000)
        await message.edit(embed=result_embed)

bot.run(TOKEN)