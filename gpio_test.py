import RPi.GPIO as gpio
import time
from discord.ext import commands


bot = commands.Bot(command_prefix = "!", case_insensitive = False)
gpio.setmode(gpio.BOARD) #use BOARD pin numbering
OUT_PIN = 19
gpio.setup(OUT_PIN, gpio.OUT)
PWM = gpio.PWM(OUT_PIN, 3) #3 hz
PWM.start(0)


@bot.command()
async def on(ctx, *args):
    PWM.ChangeDutyCycle(50) #50% duty
    await ctx.send("gpio on hopefully")

@bot.command()
async def off(ctx, *args):
    PWM.ChangeDutyCycle(0)
    await ctx.send("gpio off hopefully")

@bot.command()
async def stop(ctx, *args):
    PWM.stop()
    gpio.cleanup()
    await ctx.send("gpio stopped hopefully")


print("starting bot...")
bot.run("NTIyNTMyODQ3NDI5NjE1NjI2.DvMlgw.sVKtiF9JeYlv1gBgYWtZGAJ3UX8")
