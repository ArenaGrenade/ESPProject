import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# 100 - 300 range

temp = np.array([422, 426, 432, 444, 451, 425, 432, 454, 473, 787, 495, 526])
xtemp = np.array([3, 3, 4, 6, 7, 3, 4, 8, 11, 58, 14, 10])

func = interpolate.interp1d(xtemp, temp, "linear", fill_value="extrapolate")

print(func(15))
print(func(20))

# xdata = np.linspace(0, 119, 120)
# noise1 = (np.random.random(xdata.shape) - 0.5) * (np.random.random(xdata.shape) - 0.5) * 30
# noise2 = (np.random.random(xdata.shape)**2 - 0.5) * np.round(np.random.random(xdata.shape) * 2 - 1) * 30

# tar = np.arange(0, 120, 1)
# plt.plot(tar, func(tar) + noise1 + noise2)
# plt.show()