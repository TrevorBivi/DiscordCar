import RPi.GPIO as gpio
from picamera import PiCamera
import time
from discord.ext import commands
import discord
import asyncio


class PwmWad:

    def __init__(self, pins, freq = 100):
        gpio.setup(pins, gpio.OUT)
        self._pwms = [gpio.PWM(p, freq) for p in pins] #create all the pwms, make them all the same frequency
        for pwm in self._pwms:
            pwm.start(0) #start each pwm at 0 duty
    
    def change_duty(self, new_duty):
        for pwm in self._pwms:
            pwm.ChangeDutyCycle(new_duty)


bot = commands.Bot(command_prefix = "!", case_insensitive = False)

gpio.setmode(gpio.BOARD) #use BOARD pin numbering
OUT_PINS = (19, 21, 23, 24)
PWM = PwmWad(OUT_PINS)

cam = PiCamera()
cam.start_preview()
time.sleep(2) #HAVE TO SLEEP FOR 2 SECS TO LET THE CAMERA "WARM UP" (yeah I know its pretty nasty)


@bot.command()
async def forward(ctx, *args):
    PWM.change_duty(50)
    await ctx.send("going forward hopefully")

@bot.command()
async def backward(ctx, *args):
    PWM.change_duty(5)
    await ctx.send("going backwards hopefully")

@bot.command()
async def stop(ctx, *args):
    PWM.change_duty(0)
    await ctx.send("not moving hopefully")

@bot.command()
async def end(ctx, *args):
    PWM.stop()
    gpio.cleanup()
    msg = await ctx.send("gpio stopped hopefully")
    await ctx.send(msg.channel.id)

def take_pic():
    with open("test.jpg", "wb") as img:
        cam.capture(img)
    return "test.jpg"

async def img_spam():
    print('background process started')
    while bot.ws is None: #wait until ws connection is made (there is a short period of time after bot.run is called during which the event loop has started but a discord websocket hasn't been established)
        await asyncio.sleep(1)
    await bot.wait_until_ready() #MIGHT ACTUALLY DO THE SAME THING AS THE ABOVE LINES BUT WHATEVER
    img_channel = bot.get_channel(546361003701436426)
    print(img_channel)
    old_img_msg = None
    while True:
        img_name = take_pic()
        img_msg = await img_channel.send(file = discord.File(img_name, filename=img_name))
        if (old_img_msg is not None):
            await old_img_msg.delete()
        old_img_msg = img_msg
        await asyncio.sleep(1)
bot.loop.create_task(img_spam())

print("starting bot...")
bot.run("NTIyNTMyODQ3NDI5NjE1NjI2.DvMlgw.sVKtiF9JeYlv1gBgYWtZGAJ3UX8")
