import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from scipy.interpolate import pchip


# Import data from Excel file using pandas
df = pd.read_excel('./SMU_LI/sample2_3.3V_15C_2ns.xlsx')

# Extract columns to be used
Selion = df.iloc[:, 0]
mP = df.iloc[:, 1]

# Define duty cycle values for interpolation
T = 24
DCm = np.array([[10, 1.27490/T],
                [20, 1.64877/T],
                [30, 1.77782/T],
                [40, 1.82697/T],
                [50, 1.91134/T],
                [63, 1.9059/T]])

# print(DCm)


xq = np.arange(0, 64, 1)
print(xq)

# Interpolate duty cycle values
DC = np.interp(xq, DCm[:, 0], DCm[:, 1], left=np.nan, right=np.nan)

# DC = np.interp(DCm[:, 0], DCm[:, 1], xq)

# DC1 = np.piecewise(xq, [xq < 10, (xq >= 10) & (xq < 20), (xq >= 20) & (xq < 30), (xq >= 30) & (xq < 40),
#                        (xq >= 40) & (xq < 50), (xq >= 50) & (xq <= 63)], [1.27490/T, 1.64877/T, 1.77782/T, 1.82697/T,
#                                                                       1.91134/T, 1.9059/T])

pchip_interpolator = pchip(DCm[:, 0], DCm[:, 1])
DC1 = pchip_interpolator(xq)


# Use CubicSpline for cubic interpolation
cubic_spline = CubicSpline(DCm[:, 0], DCm[:, 1])
DC2 = cubic_spline(xq)

# mp is correct
# DC1 is correct
for i in DC:
  print(i)

# Calculate peak power
P = mP / DC1

# Plot duty cycle and peak power
plt.figure()

plt.subplot(2, 1, 1)
plt.plot(xq, DC, 'b+', xq, DC1, 'r*', xq, DC2, 'gx', DCm[:, 0], DCm[:, 1], '.')
plt.ylabel('Duty Cycle')
plt.xlabel('Selion')
plt.legend(['Interpolated DC', 'PCHIP', 'Spline', 'Measured DC'])

plt.subplot(2, 1, 2)
plt.plot(Selion, P, Selion, df.iloc[:, 6])
plt.ylabel('Peak Power')
plt.xlabel('Selion')
plt.legend(['Interpolated P', 'Measured P'])

plt.show()
