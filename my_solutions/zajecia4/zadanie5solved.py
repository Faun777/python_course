import numpy as np
from zadanie1 import animate_contour_plot
from scipy import sparse
from scipy.sparse.linalg.isolve.iterative import bicgstab
from scipy.sparse.linalg.isolve.iterative import cg

#Select linear solver by adding new name for function
solve = cg #conjugate gradient solver
# solve = bicgstab #bi-conjugate gradient stabilized solver

# Setup
size = (1., 1.)
N = 200
a = 0.01
u = np.array([-0.1, 0.])
dx = size[0]/(N-1)
dy = size[1]/(N-1)

NTimeSteps = 200

dt = 1e-1#0.5*(dx**2)/a #<-- stability requirement for time step

#Define boundary nodes
bcnodes = []
bcnodes.append(range(N)) #bottom nodes
bcnodes.append([i*N for i in range(N)]) #left nodes
bcnodes.append([(i+1)*N-1 for i in range(N)]) #right nodes
bcnodes.append([(N-1)*N + i for i in range(N)]) #top nodes
bcnodesAll = np.array(bcnodes)
bcnodesAll.reshape(bcnodesAll.size)

#Define dirichlet bounadry conditions values on each boundary
bvals = [1., 0., 0., 0.]


#Build simple equation (the same for each internal node):
equation = [-dt*a/dy**2, -dt*a/dx**2, 1 + dt*a*(2./dx**2 + 2./dy**2), -dt*a/dy**2, -dt*a/dx**2]
colShift = np.array([-N, -1, 0, 1, N])

# Create matrix in sparse format:
rowCols = [] #holds indices for non-zero columns in ith row
rowStarts=[0] #information where starts next row definition, eg. number of columns in i-th row would be rowStarts[i+1] - rowStarts[i]
data = [] # stores values for each non-zeoro coefficient in rows. Its size is the same as rowCols
for j in range(N):
    for i in range(N):
        nodeId = j*N+i
        # Equation for node at boundary
        if nodeId in bcnodesAll:
            rowCols.append(nodeId)
            data.append(1)
        else:
            # Select those parts of equation which will match matrix size
            eqparts = [i for i in range(5) if nodeId + colShift[i] >=0 and nodeId + colShift[i] < N*N]

            rowCols += [ nodeId + colShift[i] for i in eqparts ]
            data += [ equation[i] for i in eqparts ]

        rowStarts.append(len(rowCols))

#Create sparse matrix - CSR - Compressed Sparse Row Matrix
EqMat = sparse.csr_matrix((data, rowCols, rowStarts),dtype=float)

# Create and fill Rhs vector - vector holding dirichelet bc values and initital conditions
Rhs = np.zeros(N*N)

#Set inital conditions for all nodes
Rhs[:] = 1.

#Set BC conditions values to Rhs vector
for bid, bcn in enumerate(bcnodes):
    Rhs[bcn] = bvals[bid]



# Time loop
Results = list()
Results.append(np.array(Rhs.reshape((N, N))))
for iter in range(NTimeSteps):
    print('time iteration:',iter)
    sol = solve(EqMat, Rhs)

    if sol[1] != 0:
        print("solution is not converged")

    T = np.array(sol[0])
    # do not need to applay boundary conditions to Rhs, because
    # solution in T for boundary nodes is the same throughout the time.
    Rhs = T
    T = T.reshape((N, N))
    Results.append(T)


# Animate results:
animate_contour_plot(Results, skip=10, repeat=True)