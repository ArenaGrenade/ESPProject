import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

temp = np.array([10, 40, 50, 60, 60, 60, 80, 90, 60, 50, 40, 20])
xtemp = np.array([0, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119])

tar = np.arange(0, 120, 1)
func = interpolate.interp1d(xtemp, temp, "cubic", fill_value="extrapolate")

lout = []
xdata = np.linspace(0, 119, 120)
for i in range(5):
    noise1 = (np.random.random(xdata.shape) - 0.5) * (np.random.random(xdata.shape) - 0.5) * 80
    noise2 = (np.random.random(xdata.shape)**2) * np.round(np.random.random(xdata.shape)) * 50
    tout = func(tar) + noise1 + noise2
    for i in range(0, tout.shape[0], 10):
        lout.append(tout[i: i + 10].mean())
lout = np.array(lout)
plt.plot(np.arange(0, lout.shape[0], 1), lout)
a = np.array([20,18,16,13,11,14,12,15,20,22,17,18,14,11,19,18,14,11,15,14,12,20,22,18,13,12,14,19,21,16,14,11,10,8,9,9,10,8,4,3,6,5,4,3,8,5,4,4,3,3,2,1,1,0,0,0,0,0,0,0])
plt.title("TVOC in low light")
plt.plot(np.arange(0, lout.shape[0], 1), a)
plt.legend(["Light Intensity", "TVOC"])
plt.show()
