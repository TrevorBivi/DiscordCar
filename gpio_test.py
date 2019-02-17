import RPi.GPIO as gpio
from picamera import PiCamera
import time
from discord.ext import commands
import discord



bot = commands.Bot(command_prefix = "!", case_insensitive = False)

gpio.setmode(gpio.BOARD) #use BOARD pin numbering
OUT_PIN = 19
gpio.setup(OUT_PIN, gpio.OUT)
PWM = gpio.PWM(OUT_PIN, 3) #3 hz
PWM.start(0)

cam = PiCamera()
cam.start_preview()
time.sleep(2) #HAVE TO SLEEP FOR 2 SECS TO LET THE CAMERA "WARM UP" (yeah I know its pretty nasty)


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

@bot.command()
async def snap(ctx, *args):
    with open("test.jpg", "wb") as img:
        cam.capture(img)
    await ctx.send(file = discord.File("test.jpg", filename="test.jpg"))
    await ctx.send("took picture hopefully")


print("starting bot...")
bot.run("NTIyNTMyODQ3NDI5NjE1NjI2.DvMlgw.sVKtiF9JeYlv1gBgYWtZGAJ3UX8")
