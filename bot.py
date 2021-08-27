
import discord
from discord.ext import commands, tasks
from discord.utils import get


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='>', intents= intents)

client.remove_command('help')

@client.command()
async def ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)} ms")

@client.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}')

@client.command(aliases=['purge','p','c'])
async def clear(ctx, amount=1):
    perms = ctx.channel.permissions_for(ctx.author)
    if perms.manage_messages:
        await ctx.channel.purge(limit=amount+1)
    else: 
        await ctx.send("Don't  have permission to delete messages here")
    

@client.command()
async def greet(ctx, name, *,greeting):
    await ctx.send(f"{greeting} {name}")

@client.command()
async def nick(ctx, member: discord.Member, *,newname: str):
    # Gets permissions that the message sender has
    perms = ctx.channel.permissions_for(ctx.author)
    if perms.manage_nicknames:
        # If the sender can edit nicknames, edit
        await member.edit(nick=newname)
    else: 
        await ctx.send("Don't  have permissions to change nicknames")

    
@client.command(pass_context=True)
@commands.has_role("Admin") # This must be exactly the name of the appropriate role
async def giveRole(ctx,member:discord.Member,role:discord.Role):
    await member.add_roles(role)

@client.command()
async def pride(ctx):
	await ctx.send("https://tenor.com/view/pes-pesuniversity-pesu-may-the-pride-of-pes-may-the-pride-of-pes-be-with-you-gif-21274060")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Required arguments not given")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="commands", color=discord.Color.green())
    embed.add_field(name=">ping", value="To test ping", inline=False)
    embed.add_field(name=">hello", value="Mentions author and says hello", inline=False)
    embed.add_field(name=">clear or >purge or >p or >c", value="Clears the number of mesaages mention,by default it clears 1 message", inline=False)
    embed.add_field(name=">greet [name(don't ping)] [greeting]", value="Sends greeting", inline=False)
    embed.add_field(name=">nick [username or mention user] [new nickname]", value="Changes nickname", inline=False)
    embed.add_field(name=">giveRole [username or mention user] [role name]", value="To give role", inline=False)
    embed.add_field(name=">pride", value="You all know what it does", inline=False)
    embed.add_field(name=">snipe", value="Enables you to see last deleted message", inline=False)
    await ctx.send(embed=embed)

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@client.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id],color=discord.Color.red())
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except: 
        await ctx.send(f"There are no recently deleted messages here")

# keep_alive()
client.run("TOKEN")
