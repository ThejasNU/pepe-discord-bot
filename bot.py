
# importing necessary libraries
import discord
from discord.ext import commands, tasks
from discord.utils import get

# setting command prefix and Intents
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='>', intents= intents)

# removing the inbuilt help command 
client.remove_command('help')

@client.command()
async def ping(ctx):
    await ctx.send(f"Ping: {round(client.latency * 1000)} ms")

@client.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}')
    await ctx.author.send("hello,I hope you are doing good")

@client.command()
async def greet(ctx, name, *,greeting):
    await ctx.send(f"{greeting} {name}")

@client.command()
async def pride(ctx):
	await ctx.send("https://tenor.com/view/pes-pesuniversity-pesu-may-the-pride-of-pes-may-the-pride-of-pes-be-with-you-gif-21274060")

#clear command
@client.command(aliases=['purge','p','c'])
async def clear(ctx, amount=1):
    perms = ctx.channel.permissions_for(ctx.author)
    if perms.manage_messages:
        await ctx.channel.purge(limit=amount+1)
    else: 
        await ctx.send("Don't  have permission to delete messages here")
    

#changing nicknames command
@client.command()
async def nick(ctx, member: discord.Member, *,newname: str):
    # Gets permissions that the message sender has
    perms = ctx.channel.permissions_for(ctx.author)
    if perms.manage_nicknames:
        # If the sender can edit nicknames, edit
        await member.edit(nick=newname)
    else: 
        await ctx.send("Don't  have permissions to change nicknames")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Required arguments not given")

#snipe command
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

#server information command
@client.command()
async def serverinfo(ctx):
    name=ctx.guild.name
    description=ctx.guild.description
    region=ctx.guild.region
    icon=ctx.guild.icon_url
    memberCount=ctx.guild.member_count
    owner=ctx.guild.owner

    embed=discord.Embed(title=name+"Server Information",description=description,color=discord.Color.blue())
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Description",value=description,inline=False)
    embed.add_field(name="Owner",value=owner,inline=False)
    embed.add_field(name="Region",value=region,inline=False)
    embed.add_field(name="Member count",value=memberCount,inline=False)
    await ctx.send(embed=embed)

#kick command
@client.command()
@commands.has_role(834694539142103041)
async def kick(ctx,member:discord.Member,*,reason="No reason given"):
    await member.send("You were kicked from "+ctx.guild.name+". Reason: "+reason)
    await member.kick(reason=reason)

@kick.error
async def kick_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the permssion to use this command")

#ban command
@client.command()
@commands.has_role(834694539142103041)
async def ban(ctx,member:discord.Member,*,reason="No reason given"):
    await member.send("You were banned from "+ctx.guild.name+". Reason: "+reason)
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the permssion to use this command")

#unban command
@client.command()
@commands.has_role(834694539142103041)
async def unban(ctx,*,member):
    banned_members=await ctx.guild.bans()
    for person in banned_members:
        user=person.user
        if member==str(user):
            await ctx.guild.unban(user)

@unban.error
async def unban_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the permssion to use this command")

#role giving command
@client.command(pass_context=True)
@commands.has_role(834694539142103041) 
async def giveRole(ctx,member:discord.Member,role:discord.Role):
    await member.add_roles(role)

@giveRole.error
async def giveRole_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the permssion to use this command")

#contribute command
@client.command()
async def contribute(ctx):
    await ctx.send("Link has been sent in the DM")
    await ctx.author.send("If you want to contribute to pepe-bot,check this repo: https://github.com/ThejasNU/pepe-discord-bot")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="commands", color=discord.Color.green())
    embed.add_field(name=">ping", value="To test ping", inline=False)
    embed.add_field(name=">contribute", value="Sends the repo link of the bot code in DM", inline=False)
    embed.add_field(name=">hello", value="Mentions author and says hello", inline=False)
    embed.add_field(name=">greet [name or mention] [greeting]", value="Sends greeting", inline=False)
    embed.add_field(name=">pride", value="You all know what it does", inline=False)
    embed.add_field(name=">snipe", value="Enables you to see last deleted message", inline=False)
    embed.add_field(name=">serverinfo", value="Gives information of the server", inline=False)
    embed.add_field(name=">nick [username or mention user] [new nickname]", value="Changes nickname", inline=False)
    embed.add_field(name=">clear or >purge or >p or >c", value="Clears the number of mesaages mention,by default it clears 1 message", inline=False)
    embed.add_field(name=">giveRole [userid or mention user] [role name]", value="To give role", inline=False)
    embed.add_field(name=">kick [userid or mention user] [reason]", value="To kick a member", inline=False)
    embed.add_field(name=">ban [userid or mention user] [reason]", value="To ban a member", inline=False)
    embed.add_field(name=">unban [username in string form]", value="To unban a member", inline=False)
    await ctx.send(embed=embed)

TOKEN=os.environ['TOKEN']
client.run(TOKEN)
