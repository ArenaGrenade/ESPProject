import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# 100 - 300 range

temp = np.array([120, 150, 180, 200, 210, 220, 260, 240, 200, 160, 150, 130])
xtemp = np.array([9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119])

tar = np.arange(0, 120, 1)
func = interpolate.interp1d(xtemp, temp, "cubic", fill_value="extrapolate")

xdata = np.linspace(0, 119, 120)
noise1 = (np.random.random(xdata.shape) - 0.5) * (np.random.random(xdata.shape) - 0.5) * 20
noise2 = (np.random.random(xdata.shape)**2 - 0.5) * np.round(np.random.random(xdata.shape) * 2 - 1) * 20

plt.plot(tar, func(tar) + noise1 + noise2)
plt.show()

# 0 - 100 range

temp = np.array([10, 40, 50, 60, 60, 60, 80, 100, 60, 50, 40, 20])
xtemp = np.array([0, 19, 29, 39, 49, 59, 69, 79, 89, 99, 109, 119])

tar = np.arange(0, 120, 1)
func = interpolate.interp1d(xtemp, temp, "cubic", fill_value="extrapolate")

xdata = np.linspace(0, 119, 120)
noise1 = (np.random.random(xdata.shape) - 0.5) * (np.random.random(xdata.shape) - 0.5) * 20
noise2 = (np.random.random(xdata.shape)**2 - 0.5) * np.round(np.random.random(xdata.shape) * 2 - 1) * 20

plt.plot(tar, func(tar) + noise1 + noise2)
plt.show()
