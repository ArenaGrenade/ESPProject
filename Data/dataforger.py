import datetime
import numpy as np
from scipy import interpolate
import random
import matplotlib.pyplot as plt

def getTime(params, count):
    ctime = datetime.datetime(year=params["year"], month=params["month"], day=params["day"], hour=params["hour"], minute=params["minute"], second=params["second"])
    dtime = datetime.timedelta(minutes=params["delta-minute"])
    values = []
    for _ in range(count):
        tmp = str(ctime)
        values.append(tmp[:10] + "T" + tmp[11:] + "Z")
        ctime += dtime
    return values

def getTemperature(count):
    values = []
    cur = 23.3 + round(random.random() * 5, 1)
    for _ in range(int(count / 2)):
        values.append('{:.5f}'.format(round(cur, 1)))
        cur += 0.08
    for _ in range(int(count / 2)):
        values.append('{:.5f}'.format(round(cur, 1)))
        cur -= 0.08
    return values

def getHumidity(count):
    values = []
    cur = 52.1 + round(random.random() * 10, 1)
    for _ in range(count):
        values.append('{:.5f}'.format(round(cur, 1)))
        cur += random.random() - 0.5
    return values

def getLight(count, intensity="low"):
    if(intensity == "low"):
        temp = np.array([10, 40, 50, 60, 60, 60, 80, 100, 60, 50, 40, 20])
        xtemp = np.array([0, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119])
    else:
        temp = np.array([120, 150, 180, 200, 210, 220, 260, 240, 200, 160, 150, 130])
        xtemp = np.array([9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119])
    func = interpolate.interp1d(xtemp, temp, "cubic", fill_value="extrapolate")
    tar = np.arange(0, count, 1)
    noise1 = (np.random.random(tar.shape) - 0.5) * (np.random.random(tar.shape) - 0.5) * 20
    noise2 = (np.random.random(tar.shape)**2 - 0.5) * np.round(np.random.random(tar.shape) * 2 - 1) * 20
    values = func(tar) + noise1 + noise2
    return list(map(str, np.round(values, decimals=5).tolist()))

def getCO2(count, start, end):
    values = []
    cur = start + round(random.random() * 60)
    delta = (end - start) / count
    for _ in range(count):
        values.append('{:.5f}'.format(round(cur)))
        cur += delta + (random.random() - 0.5) * 8
    return values

def getTVOC(count):
    values = []
    cur = 9 + round(random.random() * 7)
    sgn = [1, -1]
    delta = [1, 2, 3, 4]
    for _ in range(count):
        values.append('{:.5f}'.format(min(abs(cur), 30)))
        cur += random.choice(sgn) * random.choice(delta)
    return values

def getVOC(count):
    values = []
    cur = 29121 + round(random.random() * 3000)
    for _ in range(count):
        values.append(str(round(cur)))
        cur += 20 + (random.random() - 0.4) * 50
    return values

def getSMS(count, start, end):
    values = []
    cur = min(98, start + round(random.random() * 10))
    delta = (end - start) / count
    for _ in range(count):
        values.append(str(round(cur)))
        cur += delta
    return values

if __name__ == "__main__":
    # print(getTime({"year": 2021, "month": 12, "day": 1, "hour": 6, "minute": 1, "second": 23, "delta-minute": 6}, 120))
    # print(getLight(120, intensity="high"))
    # print(getTemperature(120))
    # print(getHumidity(120))
    # print(getCO2(120, 452, 361))
    print(getTVOC(120))
    # print(getVOC(120))
    # print(getSMS(120, 80, 60))