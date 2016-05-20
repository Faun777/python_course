import numpy as np
import os

from resources.lab4 import of


def read_last_data(fileName):
    data = np.loadtxt(fileName)
    return data[-1][-1]

#TEST
# f = "/home/wgryglas/simflow/python_course/python_course/postProcessing/outletTotalPressure/0/faceSource.dat"
# print read_last_data(f)

of.PARAVIEW ="/opt/ParaView-4.3.1-Linux-64bit/bin/paraview"
of.OF_DIR = "/opt/openfoam231"

case = "/home/wojtek/simflow/channel_optimization"
totalPressureOutletValuse=os.path.join(case,"postProcessing","outletTotalPressure","0","faceSource.dat")


# of.createBlockMesh(case)

def loadPoints(case):
    polyMesh = os.path.join(case,"constant","polyMesh")
    pntsPath = os.path.join(polyMesh, "points")

    with open(pntsPath, "r") as pntsFile:
        l = pntsFile.readline()
        while not l.strip().isdigit():
            l = pntsFile.readline()

        size = int(l)
        pnts = np.zeros((size, 3))

        count=0

        while True:
            l = pntsFile.readline()

            if l.strip() == "(":
                continue
            elif l.strip().startswith(")"):
                break

            nums = l.replace("(","").replace(")","").strip().split()

            pnts[count,:] = map(float,nums)

            count +=1

    return pnts


def replacePoints(case, pnts):
    #copy header:
    polyMesh = os.path.join(case,"constant","polyMesh")
    pntsPath = os.path.join(polyMesh, "points")

    lines = []
    with open(pntsPath, "r") as pntsFile:
            l = pntsFile.readline()
            while not l.strip().isdigit():
                lines.append(l)
                l = pntsFile.readline()

    with open(pntsPath, "w") as f:
        f.writelines(lines)
        f.write(str(len(pnts))+"\n")
        f.write("(\n")
        for p in pnts:
            f.write("(")
            f.write(" ".join(map(str,p)))
            f.write(")\n")
        f.write(")")


def modifyMesh(params):

    points = loadPoints(case)

    #plot:
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(points[:,0], points[:,1], ".", color="green")


    tr = 0.15*np.sin(np.pi/4)
    probes = [[0.2 + tr, 0.2 - tr], [0.5 - tr, 0.2 + tr]]
    R = 0.1
    modified = []

    for i, probe in enumerate(probes):
        vecs = points[:,:2]-probe

        r1 = vecs**2
        r1 = np.sqrt(r1[:,0]+r1[:,1])/R
        nodes = r1 <= 1

        modified.append( np.array(range(len(points)))[nodes] )

        vecs = vecs[nodes,:]
        vecs[:,0] = vecs[:, 0]*(1.+r1[nodes]*params[i])
        vecs[:,1] = vecs[:, 1]*(1.+r1[nodes]*params[i])

        vecs = vecs + probe
        points[nodes,:2] = vecs


    replacePoints(case, points)

    #plot:
    plt.plot(points[:,0], points[:,1], ".")
    for probe in probes:
        plt.plot(probe[0], probe[1], "*",color="red")

    for mod in modified:
        plt.plot(points[mod,0],points[mod,1],".", color="red")

    # plt.show()



def update(params):
    of.clearResults(case)
    modifyMesh(params)
    of.runCase(case)
    return read_last_data(totalPressureOutletValuse)


#result = minimize(update, np.zeros(2), method="Nelder-Mead", options={'xtol':1e-6})

of.clearCase(case)
of.createBlockMesh(case)

#modifyMesh([0.1,0.1])

of.view(case)

