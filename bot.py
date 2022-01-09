import importlib         # used to import modules by string
import hikari, lightbulb # used to actually make the bot
import json              # used to read config file

config = json.load(open('config.json'))

modules = config["general"]["modules"]
module  = importlib.import_module("modules." + modules[0])
token   = config["discord"]["token"]

bot = lightbulb.BotApp(token=token, prefix=None, help_class=None)
ai  = module.completion(config)

@bot.command
@lightbulb.option("module", "the module to change to", choices=modules, required=True)
@lightbulb.command("module", "change the module the bot is using", guilds=[716611330198732868])
@lightbulb.implements(lightbulb.SlashCommand)
async def switchModule(ctx: lightbulb.Context) -> None:
    global ai # i am skynet and i am coming to take your babies
    module = importlib.import_module("modules." + ctx.options.module)
    ai     = module.completion(config)
    await ctx.respond(f"Changed the module to {ctx.options.module}")

@bot.command
@lightbulb.option("name", "the new name", required=False)
@lightbulb.option("backstory", "the new backstory", required=False)
@lightbulb.command("change", "change parameters of the bot", guilds=[716611330198732868])
@lightbulb.implements(lightbulb.SlashCommand)
async def change(ctx: lightbulb.Context) -> None:
    ai.changeShit(name=ctx.options.name, backstory=ctx.options.backstory)
    await ctx.respond(f"Changed the following options:\nName: {str(ctx.options.name)}\nBackstory: {str(ctx.options.backstory)}")

@bot.command
@lightbulb.command("status", "tells you the current name and backstory", guilds=[716611330198732868])
@lightbulb.implements(lightbulb.SlashCommand)
async def status(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Name: {ai.name}\nBackstory: {ai.backstory}")

@bot.command
@lightbulb.command("reset", "reset the prompt of the bot", guilds=[716611330198732868])
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx: lightbulb.Context) -> None:
    ai.changeShit() # call change without setting anything because i'm lazy and reset is gonna be a private function for now
    await ctx.respond(f"Reset!")

@bot.listen()
async def respond(event: hikari.GuildMessageCreateEvent) -> None:
    channel = str(event.get_channel())
    if event.is_bot or event.content.startswith("!ooc") or not channel in config["discord"]["channels"]: # type: ignore
        return
    else:
        user = "".join(str(event.get_member()).split("#")[:-1])
        response = ai.complete(user, event.content)
        await event.message.respond(response, reply=True, mentions_reply=False)

bot.run()
