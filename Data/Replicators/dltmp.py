import json
import datetime
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

def loadJSON(path):
    with open(path, 'r') as f:
        val = json.load(f)
    return val

def dumpJSON(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def dataToDF(data, params):
    fieldmap = {"field1": "Temperature", "field2": "Humidity", "field3": "Light", "field4": "CO2", "field5": "TVOC", "field6": "VOC", "field7": "Soil-Moisture"}
    ctime = datetime.datetime(year=params["year"], month=params["month"], day=params["day"], hour=params["hour"], minute=params["minute"], second=params["second"])
    dtime = datetime.timedelta(minutes=params["delta-minute"])
    df = pd.DataFrame(columns=["Time"] + list(fieldmap.values()))
    for point in data:
        df.loc[len(df.index)] = [point["created_at"]] + [point[key] for key in fieldmap.keys()]
        # df.loc[len(df.index)] = [str(ctime)] + [point[key] for key in fieldmap.keys()]
        ctime += dtime
    return df

def dataToDF2(data, params):
    fieldmap = {"temp": "Temperature", "hum": "Humidity", "light": "Light", "voc": "VOC", "soil": "Soil-Moisture"}
    ctime = datetime.datetime(year=params["year"], month=params["month"], day=params["day"], hour=params["hour"], minute=params["minute"], second=params["second"])
    dtime = datetime.timedelta(minutes=params["delta-minute"])
    df = pd.DataFrame(columns=["Time"] + list(fieldmap.values()))
    for point in data:
        df.loc[len(df.index)] = [point["time"]] + [point[key] for key in fieldmap.keys()]
        # df.loc[len(df.index)] = [str(ctime)] + [point[key] for key in fieldmap.keys()]
        ctime += dtime
    return df

def plotDF(df):
    xtime = range(len(df))
    fig = plt.figure(figsize=[20, 10])
    labels = df.columns
    for ind, label in enumerate(labels):
        if(ind > 0):
            ax = fig.add_subplot(240 + ind)
            ax.plot(xtime, df[label])
            ax.legend([label])
    plt.show()

data = loadJSON("./Raw/p6.json")
df = dataToDF(data, {"year": 2021, "month": 12, "day": 1, "hour": 6, "minute": 1, "second": 23, "delta-minute": 15})
# data = loadJSON("./Raw/temp.json")
# df = dataToDF2(data[0], {"year": 2021, "month": 12, "day": 1, "hour": 6, "minute": 1, "second": 23, "delta-minute": 15})
# plotDF(df)
display(df)