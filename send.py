from smtplib import SMTP
from email.mime.text import MIMEText
from email.utils import formatdate
from discord.ext import commands

class Email:
    def __init__(self, subject, to, from_, text = None):
        msg = MIMEText(text)
        msg["From"] = from_
        msg["To"] = to
        msg["Date"] = formatdate()
        msg["Subject"] = subject
        self.msg = msg

class SendEmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_full_ready(self):
        self.smtp = SMTP("smtp.gmail.com", 587)
        self.smtp.starttls()
        self.smtp.login(self.bot.data["address"], self.bot.data["passwd"])

    @commands.command()
    async def send(self, ctx, to, subject, *, content):
        email = Email(subject, to, self.bot.data["address"], content)
        self.smtp.send_message(email.msg)
        await ctx.send("送信しました")

def setup(bot):
    bot.add_cog(SendEmail(bot))