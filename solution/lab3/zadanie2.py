import numpy as np
from zadanie1 import animate_contour_plot

N = 50
delta = 1./(N-1)
a = 1.
dt = 0.1*(delta**2)/a #<-- time restriction for explicite scheme


T = np.zeros((N,N),dtype=float)

#Set bottom nodes to be equal 1
T[0,:] = 1

Results = []
time = np.linspace(0, 1, int(1./dt + 1))


forward = range(2,N)
backward = range(0,N-2)

c = a*dt/delta**2

#time loop
for t in time:
    print("time:",t)

    #Equation for new time solution - explicite euler sheme:
    # (Tn - T0)/dt -a*laplacian(T0)=0
    # Tn = T0 + a*dt*laplacian(T0)
    # Tn = T0 + (a*dt/dx**2)*(T0(i,j+1) + T0(i+1,j) - 4*T0(i,j) + T0(i-1,j) + T0(i,j-1) )

    #Loop form
    # for j in range(1, N-1):
    #     for i in range(1,N-1):
    #         T[i,j] += c * ( T[i,j+1] + T[i+1,j] - 4*T[i,j] + T[i-1,j] + T[i,j-1])

    #Vecotrized code
    T[1:-1,1:-1] = T[1:-1,1:-1] + c*(T[1:-1,forward] + T[forward,1:-1] - 4*T[1:-1,1:-1] + T[backward,1:-1] + T[1:-1,backward])

    Results.append(np.copy(T))


# Animate results:
animate_contour_plot(Results, skip=100)