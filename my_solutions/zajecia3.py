import numpy as np

# a = np.array( [i**2 for i in range(16)])
# tab2D = a.reshape((4,4))
#
# np.save("tab_a",a)
# np.save("tab_2D",tab2D)
#
# np.savetxt("tab_text",tab2D)
# np.savetxt("tab_text",a)

mapa = { "dom":1, 2:"dom2"}
# print( mapa["dom"])
# print(mapa[2])
for i in mapa:
    print(str(i)+"\t"+str(mapa[i]))
    # print(mapa[i])

def suma(a,b):
    return a+b
def roznica(a,b):
    return a-b
def iloczyn(a,b):
    return a*b
mapafunkcji = {"suma":suma, "roznica":roznica, "iloczyn":iloczyn}

a = 4
b = 8

for operacja in mapafunkcji:
    print(mapafunkcji[operacja](a,b),end="\t")
print("\n")
print( 5 in [4,2,4,5])

x,y,z = [1,2,3]

print("xyz\t"+str(x)+"\t"+str(y)+"\t"+str(z)+"\t")

def pierwiastek(a,order=2):
    return a**(1./order)
print(pierwiastek(2))
print(pierwiastek(2,4))
print(pierwiastek(2,order=100))