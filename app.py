import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

atmin_role = "Atmin"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.event
async def on_member_join(member):
    await member.send(f"Glad you're here, {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    if "hello" in message.content.lower():
        await message.channel.send(f"Hello {message.author.mention}!")
    if "bye" in message.content.lower():
        await message.channel.send(f"See ya again {message.author.mention}!")
    if "help" in message.content.lower():
        await message.channel.send("How can I assist you today?")
    if "anjing" in message.content.lower():
        await message.delete()
        await message.channel.send(f"Hey {message.author.mention} Ngga boleh kasar ya!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=atmin_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been assigned the {atmin_role}!")
    else:
        await ctx.send(f"Role {atmin_role} does not exist in this server.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=atmin_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been removed from the {atmin_role}")
    else:
        await ctx.send(f"Role {atmin_role} does not exist in this server.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("haloow!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(atmin_role)
async def atmin(ctx):
    await ctx.send(f"{ctx.author.mention} Hai atmin!")
    
@atmin.error
async def atmin_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"Sorry {ctx.author.mention}, you do not have the {atmin_role} role to use this command.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)