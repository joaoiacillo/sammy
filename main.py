import discord
import json

from re import match
from collections import namedtuple

spec = "bot.json"
spec_content = None

ParsedMessage = namedtuple('ParsedMessage', ('command', 'args'))

with open(spec, "r") as spec_file:
    spec_content = json.load(spec_file)

class Bot:
    Token = spec_content['Bot']['Token']
    ReplyForBots = spec_content['Bot'].get('ReplyForBots', False)

class Errors:
    NoSuchCommand = spec_content.get("Errors", {}).get('NoSuchCommand', "Command not found")

Commands = spec_content.get("Commands", {})

Mappings = spec_content.get("Mappings", {})

class DynamicValue:
    @staticmethod
    def is_dynamic_value(content):
        return match(r"<[^\s]+(:.*)?>", content) is not None
    
    def __init__(self, string, accepted={}) -> None:
        self.string = string
        self.accepted = accepted
        
        self.validate()
    
    def get_key(self):
        m = match(r"<([^\s:>]+)", self.string)
        return m.group(1)

    def get_value(self):
        m = match(r"[^:]*:([^>]*)>", self.string)
        if not m:
            return None
        return m.group(1).strip()
    
    def validate(self):
        key = self.get_key()
        value = self.get_value()

        if key not in self.accepted:
            raise KeyError("Unnacepted dynamic key: " + key)

        if not match(self.accepted[key], value):
            raise ValueError(f'Invalid value for key "{key}": {value}')

class MessageContext:
    def __init__(self, message: discord.Message) -> None:
        self.target = message
    
    @staticmethod
    def parse_it(content):
        args: list = content.split(' ')
        cmd = args.pop(0)
        return ParsedMessage(cmd, args)

    @staticmethod
    def get_real_cmd_name(cmd):
        if cmd in Commands:
            return cmd
        for key in Mappings:
            if cmd in Mappings[key]:
                return key
        return None

    async def take_control(self):
        parsed_message = MessageContext.parse_it(self.target.content)
        real_cmd_name = MessageContext.get_real_cmd_name(parsed_message.command)
        if real_cmd_name is None:
            await self.target.reply(Errors.NoSuchCommand.format(cmd=parsed_message.command))
        else:
            command = Commands[real_cmd_name]

            reply_message = command.get('Reply')

            if reply_message:
                await self.target.reply(reply_message.format(author=self.target.author.name))

class DefaultClient(discord.Client):
    def allows_bot_reply(self):
        return spec_content['Bot'].get('ReplyForBots', False) == True

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
    
    async def on_message(self, message: discord.Message):
        if not self.allows_bot_reply() and message.author.bot:
            return
        
        ctx = MessageContext(message)
        await ctx.take_control()


intents = discord.Intents.default()
intents.message_content = True

test = DynamicValue("<file:token>", {"file": ".+"})

def get_token():
    if DynamicValue.is_dynamic_value(Bot.Token):
        dv = DynamicValue(Bot.Token, {
            "file": r"^[\w\/\\\.,\s-]+$"
        })
        filename = dv.get_value()

        tfile = None

        try:
            tfile = open(filename, "r")
        except FileNotFoundError:
            raise ValueError(f'The file "{filename}" does not exist')
        
        token = tfile.read()
        tfile.close()
        return token
    return Bot.Token

client = DefaultClient(intents=intents)
client.run(get_token())
