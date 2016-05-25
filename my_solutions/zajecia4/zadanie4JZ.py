import numpy as np

from zadanie1 import animate_contour_plot
from kdiagonal import d_id

# Setup
N = 20
dx = 1./(N-1)
NTimeSteps = 100
a = 1.
dt = 0.01


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

# Zbierz wszystkie wezly w jeden wektor ( wykorzystaj funkcje reshape)
# skopiuj kod z poprzedniego zadania

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


#Build mass matrix
M = np.matrix(np.zeros_like(K))
M[range(N**2),range(N**2)]=1
# Uzupelnij macierz masowa

# Utworz uklad rownan
EqMatrix = M-K


# Zmodyfikuj rownania w macierzy tak, aby jawnie wprowadzic rozwiazania dla wezlow brzegowych (odwolaj sie do
# indeksow za pomoca tablicy bcnodesAll)
for i in bcnodes:
    EqMatrix[bcnodesAll,:]=0
    EqMatrix[bcnodesAll,bcnodesAll]=1

# Utworz wektor prawych stron rownania
Rhs = np.zeros(N**2)

# Zadaj warunki brzegowe i poczatkowe w wektorze prawych stron (skorzystaj z tablic bvals i bcnodes)
for wartosc_na_brzegu, ind_wezl_brzegu in zip(bvals,bcnodes):
    Rhs[ind_wezl_brzegu] = wartosc_na_brzegu


#Tworzymy zbior rozwiazan
Results = list()

#Dodajemy pierwsze rozwiazanie
Results.append(np.array(Rhs.reshape((N, N))))

# Petla czasowa
for iter in range(NTimeSteps):
    print('time iteration:',iter)

    #T = ... rozwiaz rownanie
    T = np.linalg.solve(EqMatrix,Rhs)
    # Zaktualizuj wektor prawych stron
    Rhs = T
    #Zapisz rozwiazania w liscie, na skonwertuj wyniki z wektora na tablice 2D 
    T = T.reshape((N,N))
    Results.append(T)



# Wyswietl wyniki:
animate_contour_plot(Results, skip=1, repeat=True)