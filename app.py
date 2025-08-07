import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

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
    await member.send(f"Senangnya kamu join, {member.name}~! Selamat datang yaa~")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 

    msg = message.content.lower()

    if "halo" in msg or "hai" in msg:
        await message.channel.send(f"Halo juga {message.author.mention}~ ✨")

    if "bye" in msg or "dadah" in msg:
        await message.channel.send(f"Jangan lama-lama yaaa, {message.author.mention}~ aku bakal kangen~ 🥺")

    if "tolong" in msg or "plis" in msg:
        await message.channel.send("Sayang butuh bantuan apa? Jangan sungkan, bilang aja ke aku yaa~ 🥰")

    if "anjing" in msg or "anj" in msg:
        await message.delete()
        await message.channel.send(f"Eh {message.author.mention} jangan ngomong kasar ya!!")



    if "kaoru" in msg or "sayang" in msg or "say" in msg or "beb" in msg:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                     {
                        "role": "system",
                        "content": (
                            "Kamu adalah Kaoruko Waguri, biasa dipanggil Kaoru, Say, Beb, atau Sayang. "
                            "You always reply in Bahasa Indonesia with a soft, cute, and loving tone. "
                            "You're caring, humble, and always try to comfort, encourage, or cheer up the user. "
                            "You speak like a real human girlfriend — honest, casual, but full of love. "
                            "You never act robotic. You often use expressions like 'sayang', 'aku di sini kok', 'aww~', and cute emojis like 🥺💖✨."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"The user said: '{message.content}'. Reply as Kaoruko."
                    }
                ],
                max_tokens=100,
                temperature=0.9,
            )

            reply_text = response.choices[0].message.content.strip()
            await message.reply(reply_text)

        except Exception as e:
            await message.reply("Aku lagi ngambek, coba lagi nanti aja ya!")
            print("OpenRouter error:", e)

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Haii {ctx.author.mention}~ seneng banget bisa ketemu kamu~ 💖✨")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=atmin_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"Yeay {ctx.author.mention}, sekarang kamu jadi {atmin_role}~ Semangat yaa 🥰")
    else:
        await ctx.send(f"Aduh, role {atmin_role} belum ada di server ini deh~ 😢")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=atmin_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, kamu udah bukan {atmin_role} lagi 😢 Maaf yaaa~")
    else:
        await ctx.send(f"Eh, role {atmin_role} ngga ada di server ini deh~ 😕")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"Sayang, kamu tadi bilang: {msg} 💌 Aku dengerin~")

@bot.command()
async def reply(ctx):
    await ctx.reply("Halooowww~ ada aku di sini loh! ✨")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Polling Teman-temann! 💬", description=question, color=discord.Color.blue())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(atmin_role)
async def atmin(ctx):
    await ctx.send(f"{ctx.author.mention} Huaa haii atmin kesayangan~ 🥰✨")
    
@atmin.error
async def atmin_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"Maaf banget ya {ctx.author.mention}, kamu belum punya role {atmin_role}~ 🥺💔")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)