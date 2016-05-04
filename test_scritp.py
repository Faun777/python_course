import numpy as np
import matplotlib.pyplot as plt


array = [1, 3, 5, 7, 9]

numpyArray = np.array(array)

numpyArray2 = np.sin(array) + np.cos(numpyArray)

print("some shit")


plt.figure()
plt.plot(numpyArray, numpyArray2, ".",  markersize=20)
plt.show()