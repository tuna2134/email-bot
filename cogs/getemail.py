import poplib
import email
from discord.ext import commands
from discord import Embed
from email.header import decode_header

def get_header(msg, name):
	header = ''
	if msg[name]:
		for tup in decode_header(str(msg[name])):
			if type(tup[0]) is bytes:
				charset = tup[1]
				if charset:
					header += tup[0].decode(tup[1])
				else:
					header += tup[0].decode()
			elif type(tup[0]) is str:
					header += tup[0]
	return header

def get_content(msg):
	if msg.is_multipart() is True:
		rst = ""
		for part in msg.walk():
			payload = part.get_payload(decode=True)
			if payload is None:
				continue
			charset = part.get_content_charset()
			if charset is not None:
				payload = payload.decode(charset, "ignore")
			rst += str(payload)
		return rst
	else:
		charset = msg.get_content_charset()
		payload = msg.get_payload(decode=True)
		try:
			if payload:
				if charset:
					return payload.decode(charset)
				else:
					return payload.decode()
			else:
				return ""
		except:
			return payload

class GetEmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_full_ready(self):
        self.pop = poplib.POP3_SSL('pop.gmail.com', 995)
        self.pop.user(self.bot.data["address"])
        self.pop.pass_(self.bot.data["passwd"])

    @commands.command()
    async def get(self, ctx, page:int = 1):
        content = self.pop.retr(page)[1]
        msg = email.message_from_bytes(b'\r\n'.join(content))
        e = Embed(title = get_header(msg, 'subject'), description = get_content(msg))
        await ctx.send(embed = e)

def setup(bot):
    bot.add_cog(GetEmail(bot))
