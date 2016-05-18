import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-np.pi,np.pi,1000)
y = np.linspace(-np.pi,np.pi,1000)
X,Y = np.meshgrid(x,y)
Z = np.sin(np.cos(X*Y))
# Z = np.sin(X**np.sqrt(Y))

plt.figure()
# plt.plot(X,Y,color='green')
cp = plt.contourf(X,Y,Z,200)
plt.colorbar(cp)
plt.show()