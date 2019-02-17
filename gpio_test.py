import RPi.GPIO as gpio
from picamera import PiCamera
import time
from discord.ext import commands
import discord
import asyncio


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
    msg = await ctx.send("gpio stopped hopefully")
    await ctx.send(msg.channel.id)

def take_pic():
    with open("test.jpg", "wb") as img:
        cam.capture(img)
    return "test.jpg"

#@bot.command()
#async def snap(ctx, *args):
#    img_name = take_pic()
#    msg = await ctx.send(file = discord.File(img_name, filename=img_name))
#    await ctx.send("gonna edit...")
#    img_name = take_pic
#    await msg.delete()
#    await ctx.send("edited")
#    await ctx.send("took picture hopefully")

async def img_spam():
    print('background process started')
    while bot.ws is None: #wait until ws connection is made (there is a short period of time after bot.run is called during which the event loop has started but a discord websocket hasn't been established)
        await asyncio.sleep(1)
    await bot.wait_until_ready()
    await asyncio.sleep(10)
    img_channel = bot.get_channel(546361003701436426) 
    print(img_channel)
    img_msg = None
    while True:
        img_name = take_pic()
        if (img_msg is not None):
            img_msg.delete()
        img_msg = await img_channel.send(file = discord.File(img_name, filename=img_name))
        await asyncio.sleep(1)
bot.loop.create_task(img_spam())

print("starting bot...")
bot.run("NTIyNTMyODQ3NDI5NjE1NjI2.DvMlgw.sVKtiF9JeYlv1gBgYWtZGAJ3UX8")
