import numpy as np
from zadanie1 import animate_contour_plot
from kdiagonal import d_id
from numpy.linalg import solve



N = 50

# Definicja numerow wezlow brzegowych w pelnym wektorze rozwiazan T o wymiarze N*N
bcnodes = []
bcnodesAll = []
    #dolne wezly
bcnodes.append(range(N))
bcnodesAll.extend(range(N))
    #wezly na lewo
bcnodes.append(range(N,(N-1)*N,N))
bcnodesAll.extend(range(N,(N-1)*N,N))
    #wezly na prawo
bcnodes.append(range(N-1,N*N-1,N))
bcnodesAll.extend(range(2*N-1,N*N-1,N))
    #wezly na scianie gornej
bcnodes.append(range((N-1)*N,N*N-1,1))
bcnodesAll.extend(range((N-1)*N,N*N-2,1))
print("bcnodes = "+str(bcnodes))
print("bcnodes2 = "+str(np.array(bcnodes).flatten()))
print(i for i in bcnodes)
# Zbierz wszystkie wezly w jeden wektor ( wykorzystaj funkcje reshape)
#bcnodesAll = ... twoj kod ...


#Zdefiniuj wartosci rozwiazania dla kazdego z 4 brzegow
bvals = [1,0,0,0]

#Zbuduj uklad rownan uzupelniajac elementy macierzy K
K = np.matrix(np.zeros((N**2, N**2)))

 # Diagonala odnoszaca sie do wezlow T[i,j-1]
K[d_id(K,-N)]=1
 # Diagonala odnoszaca sie do wezlow T[i-1,j]
# twoj kod ....
K[d_id(K,-1)]=1
 # Glowna diagonala, wezlu T[i,j]
K[range(N**2),range(N**2)]=-4
 # Diagonala odnoszaca sie do wezlow T[i+1,j]
K[d_id(K,1)]=1
 # Diagonala odnoszaca sie do wezlow T[i,j+1]
K[d_id(K,N)]=1

print(K)

# Zmodyfikuj rownania w macierzy tak, aby jawnie wprowadzic rozwiazania dla wezlow brzegowych (odwolaj sie do
# indeksow za pomoca tablicy bcnodesAll)
for i in bcnodes:
    K[bcnodesAll,:]=0
    K[bcnodesAll,bcnodesAll]=1
print(K)

# Utworz wektor prawych stron rownania
Rhs = np.zeros(N**2)

# Zadaj warunki brzegowe w wektorze prawych stron (skorzystaj z tablic bvals i bcnodes)
for wartosc_na_brzegu, ind_wezl_brzegu in zip(bvals,bcnodes):
    Rhs[ind_wezl_brzegu] = wartosc_na_brzegu

print(Rhs)
# Rozwiaz rownanie
T = np.array( solve(K, Rhs) )

# Rebuild T to 2D array
T = T.reshape((N,N))
print("\n"+"T")
print(T)
# Plot result
animate_contour_plot([T])