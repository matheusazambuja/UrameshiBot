import discord
from discord.ext import commands
from jikanpy import Jikan
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from services import utils
from services.anime import anime
from services.search import search
from services.schedule import schedule

PREFIX = '!'

load_dotenv('env')
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.command(name='disconnect')
async def cmd_disconnect(ctx):
    await bot.close()


@bot.command(name='info')
async def cmd_info(ctx):
    embed = discord.Embed(
        title='Info menu!', description="Server's informations", 
        timestamp=datetime.utcnow(), color=discord.Color.green()
    )

    embed.add_field(name='Server created at', value=f'{ctx.guild.created_at}', inline=False)
    embed.add_field(name='Server owner', value=f'{ctx.guild.owner}', inline=False)
    embed.add_field(name='Server Region', value=f'{ctx.guild.region}', inline=False)
    embed.add_field(name='Server ID', value=f'{ctx.guild.id}', inline=False)

    embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name='help')
async def cmd_help(ctx):
    embed = discord.Embed(
        title=f' :rainbow:  Urameshi - Help!',
        description='A simple bot for anime informations',
        color=discord.Color.green()
    )

    embed.add_field(name=f'- Command: ```{PREFIX}info```', value="Server's informations from this server", inline=False)
    embed.add_field(name=f'- Command: ```{PREFIX}songs```', value='Name of openings and closings of the researched anime', inline=False)
    embed.add_field(name=f'- Command: ```{PREFIX}broadcast```', value='Anime broadcast time', inline=False)
    embed.add_field(name=f'- Command: ```{PREFIX}schedule```', value='Anime schedule for someday in this season (Input week of day)', inline=False)
    embed.add_field(name=f'- Command: ```{PREFIX}seasons```', value="Animes season prequel and sequel", inline=False)

    embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name='songs', help='Name of openings and closings of the researched anime')
async def cmd_songs(ctx, *name: str):
    anime_found = search(' '.join(name))
    if anime_found['found']:
        anime_found = anime(anime_found['id'], 'songs')
        if anime_found['found']:
            embed = discord.Embed(
                title=f' :loud_sound:  {anime_found["title"]} ({anime_found["title_japanese"]})',
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=anime_found['image_url'])

            list_openings_strings = '\n'.join([f"Name: {op}" for op in anime_found['op']])
            embed.add_field(name=f'-- Openings: --', value=f"```{list_openings_strings}```", inline=False)

            embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

            embed = discord.Embed(
                title=f' :loud_sound:  {anime_found["title"]} ({anime_found["title_japanese"]})',
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=anime_found['image_url'])

            list_ending_strings = '\n'.join([f"Name: {end}" for end in anime_found['end']])
            embed.add_field(name=f'-- Endings: --', value=f"```{list_ending_strings}```", inline=False)

            embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

    if not anime_found['found']:
        await ctx.send(utils.help_messages(anime_found['error']))



@bot.command(name='schedule', help='Anime schedule for someday in this season (Input week of day)')
async def cmd_schedule(ctx, *day: str):
    animes_today = schedule(' '.join(day))
    if animes_today['found']:
        for anime in animes_today['results']:
            embed = discord.Embed(
                title=f' :popcorn:  {anime["title"]}', 
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=anime['image_url'])

            if anime["synopsis"] and len(anime["synopsis"]) > 1022:
                synopsis = anime['synopsis']
                list_synopsis = []
                while len(synopsis) > 1000:
                    list_synopsis.append(synopsis[0:999])
                    synopsis = synopsis[1000:]

                list_synopsis.append(synopsis)
                for s in list_synopsis:
                    embed.add_field(name=f':books:  Synopsis:', value=f'```{s}```', inline=False)
            else:
                embed.add_field(name=f':books:  Synopsis:', value=f'```{anime["synopsis"]}```', inline=False)

            embed.add_field(name=f'Genres:', value=f'```{", ".join([g["name"] for g in anime["genres"]])}```', inline=False)
            embed.add_field(name=f':globe_with_meridians:  Link Mal (Myanimelist.net):', value=f'```{anime["url"]}```', inline=False)

            embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed=embed)
    else:
        await ctx.send(utils.help_messages(animes_today['error']))
        


@bot.command(name='seasons', help='Animes season prequel and sequel')
async def cmd_season(ctx, *name: str):
    anime_found = search(' '.join(name))
    if anime_found['found']:

        anime_found = anime(anime_found['id'], 'seasons')
        if anime_found['found']:
            while anime_found['found'] and 'Prequel' in anime_found['related']:
                anime_found = anime(anime_found['related']['Prequel'][0]['mal_id'], 'seasons')

            while anime_found['found'] and 'Sequel' in anime_found['related']:
                if anime_found['airing']:
                    embed = discord.Embed(
                        title=f' :popcorn:  {anime_found["title"]} ' + f'({anime_found["title_japanese"]})',
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=anime_found['image_url'])

                    embed.add_field(name=f'  Type:', value=f'```{anime_found["type"]}```', inline=False)
                    embed.add_field(name=f':hourglass_flowing_sand:  Status:', value=f'```{anime_found["status"]}```', inline=False)

                    if anime_found['premiered']:
                        emoji_season = utils.emoji(anime_found['premiered'])
                        embed.add_field(name=f'- {emoji_season}  Season:', value=f'```{anime_found["premiered"]}```', inline=False)

                    embed.add_field(name=f':ballot_box_with_check:  Total Episodes:', value=f'```{anime_found["episodes"]}```', inline=False)
                    embed.add_field(name=f':watch:  Broadcast in Japan:', value=f'```{anime_found["broadcast"]}```', inline=False)
                    embed.add_field(name=f':globe_with_meridians:  Link Mal (Myanimelist.net):', value=f'```{anime_found["url"]}```', inline=False)

                    embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                else:
                    embed = discord.Embed(
                        title=f' :popcorn:  {anime_found["title"]} ' + f'({anime_found["title_japanese"]})',
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=anime_found['image_url'])

                    embed.add_field(name=f'  Type:', value=f'```{anime_found["type"]}```', inline=False)
                    embed.add_field(name=f':hourglass:  Status:', value=f'```{anime_found["status"]}```', inline=False)

                    if anime_found['premiered']:
                        emoji_season = utils.emoji(anime_found['premiered'])
                        embed.add_field(name=f'- {emoji_season}  Season:', value=f'```{anime_found["premiered"]}```', inline=False)

                    embed.add_field(name=f':ballot_box_with_check:  Total Episodes:', value=f'```{anime_found["episodes"]}```', inline=False)
                    embed.add_field(name=f':globe_with_meridians:  Link Mal (Myanimelist.net):', value=f'```{anime_found["url"]}```', inline=False)

                    embed.set_footer( text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

                await ctx.send(embed=embed)
                anime_found = anime(anime_found['related']['Sequel'][0]['mal_id'], 'seasons')

    if not anime_found['found']:
        await ctx.send(utils.help_messages(anime_found('error')))


@bot.command(name='broadcast', help='Anime broadcast time')
async def cmd_broadcast(ctx, *name: str):
    anime_found = search(' '.join(name))
    if anime_found['found']:
        anime_found = anime(anime_found['id'], 'broadcast')

        if anime_found['found']:
            emoji_season = utils.emoji(anime_found['premiered'])

            if anime_found['airing']:
                embed = discord.Embed(
                    title=f' :popcorn:  {anime_found["title"]} ' + f'({anime_found["title_japanese"]})',
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=anime_found['image_url'])

                embed.add_field(name=f':hourglass_flowing_sand:  Status:', value=f'```{anime_found["status"]}```', inline=False)
                embed.add_field(name=f'{emoji_season}  Season:', value=f'```{anime_found["premiered"]}```', inline=False)
                embed.add_field(name=f':ballot_box_with_check:  Total Episodes:', value=f'```{anime_found["episodes"]}```', inline=False)
                embed.add_field(name=f':watch:  Broadcast in Japan:', value=f'```{anime_found["broadcast"]}```', inline=False)
                embed.add_field(name=f':globe_with_meridians:  Link Mal (Myanimelist.net):', value=f'```{anime_found["url"]}```', inline=False)

                embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            else:
                embed = discord.Embed(
                    title=f' :popcorn:  {anime_found["title"]} ' + f'({anime_found["title_japanese"]})',
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=anime_found['image_url'])

                embed.add_field(name=f':hourglass:  Status:', value=f'```{anime_found["status"]}```', inline=False)
                embed.add_field(name=f'{emoji_season}  Season:', value=f'```{anime_found["premiered"]}```', inline=False)
                embed.add_field(name=f':ballot_box_with_check:  Total Episodes:', value=f'```{anime_found["episodes"]}```', inline=False)
                embed.add_field(name=f':globe_with_meridians:  Link Mal (Myanimelist.net):', value=f'```{anime_found["url"]}```', inline=False)

                embed.set_footer(text='Requested by ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed=embed)

    if not anime_found['found']:
        await ctx.send(utils.help_messages(anime_found('error')))


bot.run(TOKEN)