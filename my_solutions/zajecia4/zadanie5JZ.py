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

# Definicja numerow wezlow brzegowych w pelnym wektorze rozwiazan T o wymiarze N*N
# skopiuj kod z poprzedniego zadania

# Zbierz wszystkie wezly w jeden wektor ( wykorzystaj funkcje reshape)
# skopiuj kod z poprzedniego zadania

#Zdefiniuj wartosci rozwiazania dla kazdego z 4 brzegow
# skopiuj kod z poprzedniego zadania


# Skonstruuj macierz ukladu rownan wykorzystujac format macierzy rzadkich
rowCols = [] #holds indices for non-zero columns in ith row
rowStarts=[0] #information where starts next row definition, eg. number of columns in i-th row would be rowStarts[i+1] - rowStarts[i]
data = [] # stores values for each non-zeoro coefficient in rows. Its size is the same as rowCols
# Twoj kod ....

#Create sparse matrix - CSR - Compressed Sparse Row Matrix
EqMat = sparse.csr_matrix((data, rowCols, rowStarts),dtype=float)

# Create and fill Rhs vector - vector holding dirichelet bc values and initital conditions
Rhs = np.zeros(N*N)

# Zadaj warunki brzegowe i poczatkowe w wektorze prawych stron (skorzystaj z tablic bvals i bcnodes)
# Twoj kod ....


# Time loop
Results = list()
Results.append(np.array(Rhs.reshape((N, N))))


for iter in range(NTimeSteps):
    print 'time iteration:',iter

    sol = solve(EqMat, Rhs)

    if sol[1] != 0:
        print "solution is not converged"

    T = np.array(sol[0])

    # Zaktualizuj wektor prawych stron
    #Rhs = ....

    #Zapisz rozwiazania w liscie, na skonwertuj wyniki z wektora na tablice 2D
    # T = ... twoj kod ..
    Results.append(T)


# Animate results:
animate_contour_plot(Results, skip=10, repeat=True)