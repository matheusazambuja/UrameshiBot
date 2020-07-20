import discord
from discord.ext import commands
from jikanpy import Jikan
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from random import choice


prefix = '!'

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help"))


@bot.command(name='disconnect')
async def disconnect(ctx):
    await bot.close()


@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(
        title='Info menu!',
        description="Server's informations",
        timestamp=datetime.utcnow(),
        color=discord.Color.green())
    embed.add_field(
        name='Server created at',
        value=f'{ctx.guild.created_at}',
        inline=False)
    embed.add_field(
        name='Server owner',
        value=f'{ctx.guild.owner}',
        inline=False)
    embed.add_field(
        name='Server Region',
        value=f'{ctx.guild.region}',
        inline=False)
    embed.add_field(
        name='Server ID',
        value=f'{ctx.guild.id}',
        inline=False)
    embed.set_footer(
        text='Requested by ' + ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title=f' :rainbow:  Urameshi - Help!',
        description='A simple bot for anime informations',
        color=discord.Color.green())
    embed.add_field(
        name=f'- Command: ```{prefix}info```',
        value="Server's informations from this server",
        inline=False)
    embed.add_field(
        name=f'- Command: ```{prefix}99```',
        value='Quotes by 99',
        inline=False)
    embed.add_field(
        name=f'- Command: ```{prefix}songs```',
        value='Name of openings and closings of the researched anime',
        inline=False)
    embed.add_field(
        name=f'- Command: ```{prefix}broadcast```',
        value='Anime broadcast time',
        inline=False)
    embed.set_footer(
        text='Requested by ' + ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quoted = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = choice(brooklyn_99_quoted)
    await ctx.channel.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='songs', help='Name of openings and closings of the researched anime')
async def songs(ctx, *name: str):
    jikan = Jikan()
    animes_researched = jikan.search(search_type='anime', query=' '.join(name))

    if animes_researched:
        first_anime = animes_researched['results'][0]
        anime_found = jikan.anime(first_anime['mal_id'])
        embed = discord.Embed(
            title=f' :loud_sound:  {anime_found["title"]} ({anime_found["title_japanese"]})',
            color=discord.Color.green())
        embed.set_thumbnail(url=anime_found['image_url'])
        str_op = '\n'.join(
            [f"Name: {op}" for op in anime_found['opening_themes']])
        embed.add_field(
            name=f'-- Openings: --',
            value=f"```{str_op}```",
            inline=False)
        embed.set_footer(
            text='Requested by ' + ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

        embed = discord.Embed(
            title=f' :loud_sound:  {anime_found["title"]} ({anime_found["title_japanese"]})',
            color=discord.Color.green())
        embed.set_thumbnail(url=anime_found['image_url'])
        str_end = '\n'.join(
            [f"Name: {end}" for end in anime_found['ending_themes']])
        embed.add_field(
            name=f'-- Endings: --',
            value=f"```{str_end}```",
            inline=False)
        embed.set_footer(
            text='Requested by ' + ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    else:
        await ctx.send('```No results for this anime```')


@bot.command(name='broadcast', help='Anime broadcast time')
async def broadcast(ctx, *name: str):
    jikan = Jikan()
    animes_researched = jikan.search(search_type='anime', query=' '.join(name))

    if animes_researched:
        first_anime = animes_researched['results'][0]
        anime_found = jikan.anime(first_anime['mal_id'])

        dict_emojis = {
            'Fall': ':fallen_leaf:',
            'Spring': ':sunflower:',
            'Summer': ':sunrise:',
            'Winter': ':cloud_snow:'
        }
        emoji = [emoji for season, emoji in dict_emojis.items() if season in anime_found['premiered']]
        if emoji:
            emoji_season = emoji[-1]
        else:
            emoji_season = ''

        if anime_found['airing']:
            embed = discord.Embed(
                title=f' :popcorn:  {anime_found["title"]} ' +
                      f'({anime_found["title_japanese"]})',
                color=discord.Color.green())
            embed.set_thumbnail(url=anime_found['image_url'])
            embed.add_field(
                name=f'- :hourglass_flowing_sand:  Status:',
                value=f'```{anime_found["status"]}```',
                inline=False)
            embed.add_field(
                name=f'- {emoji_season}  Season:',
                value=f'```{anime_found["premiered"]}```',
                inline=False)
            embed.add_field(
                name=f'- Total Episodes:',
                value=f'```{anime_found["episodes"]}```',
                inline=False)
            embed.add_field(
                name=f'- :watch:  Broadcast in Japan:',
                value=f'```{anime_found["broadcast"]}```',
                inline=False)
            embed.add_field(
                name=f'- :globe_with_meridians:  Link Mal (Myanimelist.net):',
                value=f'```{anime_found["url"]}```',
                inline=False)
            embed.set_footer(
                text='Requested by ' + ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url)
        else:
            embed = discord.Embed(
                title=f' :popcorn:  {anime_found["title"]} ' +
                      f'({anime_found["title_japanese"]})',
                color=discord.Color.green())
            embed.set_thumbnail(url=anime_found['image_url'])
            embed.add_field(
                name=f'- :hourglass:  Status:',
                value=f'```{anime_found["status"]}```',
                inline=False)
            embed.add_field(
                name=f'- {emoji_season}  Season:',
                value=f'```{anime_found["premiered"]}```',
                inline=False)
            embed.add_field(
                name=f'- Total Episodes:',
                value=f'```{anime_found["episodes"]}```',
                inline=False)
            embed.add_field(
                name=f'- :globe_with_meridians:  Link Mal (Myanimelist.net):',
                value=f'```{anime_found["url"]}```',
                inline=False)
            embed.set_footer(
                text='Requested by ' + ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f'```No results for this anime```')


bot.run(TOKEN)
