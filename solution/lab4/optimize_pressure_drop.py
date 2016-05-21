import numpy as np
import os
import matplotlib.pyplot as plt
from resources.lab4 import of
import shutil
from scipy import optimize

def read_last_data(fileName):
    data = np.loadtxt(fileName)
    return data[-1][-1]

#TEST
# f = "/home/wgryglas/simflow/python_course/python_course/postProcessing/outletTotalPressure/0/faceSource.dat"
# print read_last_data(f)

of.PARAVIEW ="/opt/ParaView-4.3.1-Linux-64bit/bin/paraview"
of.OF_DIR = "/opt/openfoam231"

case = "/home/wojtek/simflow/channel_optimization"
totalPressureOutletValues=os.path.join(case,"postProcessing","outletTotalPressure","0","faceSource.dat")
totalPressureInletValues=os.path.join(case,"postProcessing","inletTotalPressure","0","faceSource.dat")


def copyPoints(case, fname):
    polyMesh = os.path.join(case,"constant","polyMesh")
    pntsPath = os.path.join(polyMesh, "points")
    pntsNewPath = os.path.join(polyMesh, fname)
    if not os.path.exists(pntsNewPath):
        shutil.copy(pntsPath, pntsNewPath)

def loadPoints(case, fname):
    polyMesh = os.path.join(case,"constant","polyMesh")
    pntsPath = os.path.join(polyMesh, fname)

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


def modifyPoints1(params, points):
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

        #plot:
        plt.plot(points[:,0], points[:,1], ".")
        for probe in probes:
            plt.plot(probe[0], probe[1], "*",color="red")

        for mod in modified:
            plt.plot(points[mod,0],points[mod,1],".", color="red")

    return points

def modifyPoints2(params, points):

    modifers = [ [ [0.2, 0.2], (points[:,0] > 0.2)*(points[:,1] < 0.2),[np.sqrt(2)/2, -np.sqrt(2)/2] ],\
                 [ [0.5, 0.2], (points[:,0] < 0.5)*(points[:,1] > 0.2),[-np.sqrt(2)/2, np.sqrt(2)/2] ] ]

    for mod, p in zip(modifers,params):
        center, nodes, middle = mod

        centerLine = points[nodes,:2] - center

        centerLineNorm = np.copy(centerLine)
        centerLineNorm[:,0] = centerLineNorm[:,0]/ np.sqrt(centerLine[:,0]**2 + centerLine[:,1]**2)
        centerLineNorm[:,1] = centerLineNorm[:,1]/ np.sqrt(centerLine[:,0]**2 + centerLine[:,1]**2)

        centerLine = centerLineNorm * 0.15 + center

        angScale = centerLineNorm[:,0]*middle[0] + centerLineNorm[:,1]*middle[1] - np.sqrt(2)/2

        fromCenterLine = points[nodes,:2] - centerLine

        points[nodes, 0] = centerLine[:, 0] + fromCenterLine[:, 0]*(1+angScale*p)
        points[nodes, 1] = centerLine[:, 1] + fromCenterLine[:, 1]*(1+angScale*p)

        # plt.plot(points[nodes,0], points[nodes,1], ".", color="red")


def modifyMesh(params):

    points = loadPoints(case, "points_source")

    #plot:
    # plt.figure()
    # plt.plot(points[:,0], points[:,1], ".", color="green")

    modifyPoints2(params, points)

    replacePoints(case, points)

    # plt.show()


iterations =[]

pictures="/home/wojtek/Documents/studia-doktoranckie/myccfd-courses/figures/python_inst05/optianimation"

def update(params):
    of.clearResults(case)
    modifyMesh(params)

    of.runCase(case, output=False)

    inletPtotalIntegral = read_last_data(totalPressureInletValues)
    outletPtotalIntegral = read_last_data(totalPressureOutletValues)

    objective= inletPtotalIntegral- outletPtotalIntegral
    iterations.append(objective)

    of.saveCurrentImage(os.path.join(pictures,str(len(iterations))+".png"), case, colorby="U")#"total(p)"

    print objective
    return objective


if not of.hasMesh(case):
    of.createBlockMesh(case)

copyPoints(case,"points_source")

result = optimize.fmin(update, [0.05, 0.05]) #, maxiter=12 #
#result = optimize.minimize(update, [0.1, 0.1], method="Nelder-Mead", options={'xtol':1e-6, 'maxiter':100})

# plt.figure()
# plt.plot(iterations)
# plt.title("Difference of inlet and outlet total pressure integrals")
# plt.xlabel("Iteration No")
# plt.ylabel("Integrall difference")
# plt.grid(True)
# plt.show()

#of.view(case)


