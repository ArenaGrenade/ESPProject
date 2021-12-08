from datatts import toThingSpeak
from dataforger import *


for day in range(1, 6):
    count = 120
    times = getTime(params={"year": 2021, "month": 12, "day": day, "hour": 6, "minute": 1, "second": 23, "delta-minute": 6}, count=count)
    temperature = getTemperature(count=count)
    humidity = getHumidity(count=count)
    light = getLight(count=count, intensity="high")
    co2 = getCO2(count=count, start=457, end=321)
    tvoc = getTVOC(count=count)
    voc = getVOC(count=count)
    moisture = getSMS(count=count, start=81, end=35)

    tts = toThingSpeak(["created_at", "entry_id", "field1", "field2", "field3", "field4", "field5", "field6", "field7"])
    for i in range(count):
        tts.add([times[i], i + 1, temperature[i], humidity[i], light[i], co2[i], tvoc[i], voc[i], moisture[i]])
    tts.save("Synthetic/log_dec" + str(day) + ".json")