from datatts import toThingSpeak
from dataforger import *

count = 120
times = getTime(params={"year": 2021, "month": 12, "day": 1, "hour": 6, "minute": 1, "second": 23, "delta-minute": 6}, count=count)
temperature = getTemperature(count=count)
humidity = getHumidity(count=count)
light = getLight(count=count, intensity="high")
moisture = getSMS(count=count, start=91, end=35)

tts = toThingSpeak(["created_at", "entry_id", "field1", "field2", "field3", "field7"])
for i in range(count):
    tts.add([times[i], i + 1, temperature[i], humidity[i], light[i], moisture[i]])
# tts.print(1)
tts.save("Synthetic/log1.json")