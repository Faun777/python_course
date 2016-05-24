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

of.PARAVIEW ="/home/wgryglas/Applications/ParaView-4.3.1-Linux-64bit/bin/paraview"#"/opt/ParaView-4.3.1-Linux-64bit/bin/paraview"
of.OF_DIR = "/opt/openfoam30"

resourcesPath="/home/wgryglas/Documents/dydaktyka/python_course/resources"
casePath = "/home/wgryglas/simflow/channel_optimization"
totalPressureOutletValues=os.path.join(casePath,"postProcessing","outletTotalPressure","0","faceSource.dat")
totalPressureInletValues=os.path.join(casePath,"postProcessing","inletTotalPressure","0","faceSource.dat")


def copyPoints(case, fname):
    polyMesh = os.path.join(case,"constant","polyMesh")
    pntsPath = os.path.join(polyMesh, "points")
    pntsNewPath = os.path.join(polyMesh, fname)
    #if not os.path.exists(pntsNewPath):
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


class PointDisplacement:
    def __init__(self, case, resources):
        self.case = case
        self.resources = resources

    def init(self):
        dictSource = os.path.join(self.resources, "lab4", "channel_optimization", "constant", "polyMesh", "blockMeshDict")
        dictDest = os.path.join(self.case, "constant", "polyMesh", "blockMeshDict")
        shutil.copy(dictSource, dictDest)
        of.createBlockMesh(casePath)
        self.points = loadPoints(self.case, "points")

    def modify(self, params):
        nPnts = np.copy(self.points)
        self.__modify__(params, nPnts)
        replacePoints(self.case, nPnts)

    def __modify__(self, params, points):
        pass

class TwoParameterDisplacement(PointDisplacement):
    def __init__(self, case, resources):
        #super(TwoParameterDisplacement, self).__init__(case, resources)
        PointDisplacement.__init__(self, case, resources)

    def __modify__(self, params, points):
        params = params[:2]
        modifers = [ [ [0.2, 0.2], (points[:,0] > 0.2)*(points[:,1] < 0.2),[np.sqrt(2)/2, -np.sqrt(2)/2] ],\
                 [ [0.5, 0.2], (points[:,0] < 0.5)*(points[:,1] > 0.2),[-np.sqrt(2)/2, np.sqrt(2)/2] ] ]

        for mod, p in zip(modifers, params[:2]):
            center, nodes, middle = mod

            centerLine = points[:,:2] - center

            centerLineNorm = np.copy(centerLine)
            centerLineNorm[:,0] = centerLineNorm[:,0]/ np.sqrt(centerLine[:,0]**2 + centerLine[:,1]**2)
            centerLineNorm[:,1] = centerLineNorm[:,1]/ np.sqrt(centerLine[:,0]**2 + centerLine[:,1]**2)

            centerLine = centerLineNorm * 0.15 + center

            angScale = (centerLineNorm*middle).sum(axis=1) - np.sqrt(2)/2

            fromCenterLine = points[:,:2] - centerLine

            points[nodes, 0] = centerLine[nodes, 0] + fromCenterLine[nodes, 0]*(1+angScale[nodes]*p)
            points[nodes, 1] = centerLine[nodes, 1] + fromCenterLine[nodes, 1]*(1+angScale[nodes]*p)


class FourParmaeterDisplacement(PointDisplacement):
    def __init__(self,case, resources):
        #super(FourParmaeterDisplacement, self).__init__(case, resources)
        PointDisplacement.__init__(self, case, resources)

    def __modify__(self, params, points):
        params = params[:4]
        modifers = [ [ [0.2, 0.2], (points[:,0] > 0.2)*(points[:,1] < 0.2),[np.sqrt(2)/2, -np.sqrt(2)/2] ],\
                 [ [0.5, 0.2], (points[:,0] < 0.5)*(points[:,1] > 0.2),[-np.sqrt(2)/2, np.sqrt(2)/2] ] ]

        joinedP = [params[:2], params[2:]]

        for mod, param in zip(modifers, joinedP):
            center, nodes, middle = mod

            centerLine = points[:,:2] - center

            centerLineNorm = np.copy(centerLine)
            centerLineNorm[:,0] = centerLineNorm[:,0]/ np.sqrt(centerLine[:,0]**2 + centerLine[:,1]**2)
            centerLineNorm[:,1] = centerLineNorm[:,1]/ np.sqrt(centerLine[:,0]**2 + centerLine[:,1]**2)

            centerLine = centerLineNorm * 0.15 + center

            angScale = (centerLineNorm*middle).sum(axis=1) - np.sqrt(2)/2

            fromCenterLine = points[:,:2] - centerLine

            side = (fromCenterLine*centerLineNorm).sum(axis=1)

            sides = [side > 0, side <= 0]

            for s, p in zip(sides, param):
                s = s*nodes
                points[s, 0] = centerLine[s, 0] + fromCenterLine[s, 0]*(1+angScale[s]*p)
                points[s, 1] = centerLine[s, 1] + fromCenterLine[s, 1]*(1+angScale[s]*p)


def replaceTemplates(source, dest, replacementDict):
    with open(source,"r") as r:
        with open(dest,"w") as w:
            for l in r:
                for k in replacementDict:
                    check = "__"+k+"__"
                    if check in l:
                        l = l.replace(check, str(replacementDict[k]) )#"%.6lf"%replacementDict[k]
                w.write(l)

class ChangeRadiusKeepTangent:
    def __init__(self, case, resourcesPath):
        self.case = case
        self.resources = resourcesPath

    def init(self):
        pass

    def modify(self, rads):
        from scipy.optimize import newton_krylov

        r1, r2 = rads[:2]
        p1 = np.array([0.2, 0])
        p2 = np.array([0.2, 0.1])
        p6 = np.array([0.5, 0.3])
        p7 = np.array([0.5, 0.4])

        c1 = p2 + [0, r1]
        c2 = p1 + [0, r2]

        def eqRads(params):
            r3, r4 = params
            c3 = p6 - [0, r3]
            c4 = p7 - [0, r4]
            F = np.zeros(len(params))
            F[0] = (c1-c4).dot(c1-c4) - (r1+r4)**2
            F[1] = (c2-c3).dot(c2-c3) - (r2+r3)**2
            return F

        r3, r4 = newton_krylov(eqRads,[0, 0])

        c3 = p6 - [0, r3]
        c4 = p7 - [0, r4]

        def eqMids(params):
            p4x, p4y, p5x, p5y = params
            p4 = np.array([p4x,p4y])
            p5 = np.array([p5x,p5y])

            F = np.zeros(len(params))
            F[0] = (p5-c1).dot(p5-c1) - r1**2
            F[1] = (p5-c4).dot(p5-c4) - r4**2
            F[2] = (p4-c2).dot(p4-c2) - r2**2
            F[3] = (p4-c3).dot(p4-c3) - r3**2
            return F
        p4x, p4y, p5x, p5y = newton_krylov(eqMids,[p1[0], p1[1], p2[0], p2[1]], x_tol=1e-4)


        p4 = np.array([p4x, p4y])
        p5 = np.array([p5x, p5y])
        c3 = p6 - [0, r3]
        c4 = p7 - [0, r4]

        p10 = p2+(p5-p2)/2-c1
        p10 = c1 + p10/np.sqrt(p10.dot(p10))*r1

        p11 = p1+(p4-p1)/2-c2
        p11 = c2 + p11/np.sqrt(p11.dot(p11))*r2

        p12 = p4+(p6-p4)/2-c3
        p12 = c3 + p12/np.sqrt(p12.dot(p12))*r3

        p13 = p5+(p7-p5)/2-c4
        p13 = c4 + p13/np.sqrt(p13.dot(p13))*r4

        src = os.path.join(self.resources,"lab4","channel_optimization","constant","polyMesh","blockMeshDict_template")
        dst = os.path.join(casePath,"constant","polyMesh","blockMeshDict")
        rep = {"p4x":p4x, "p4y":p4y, "p5x":p5x, "p5y":p5y, \
               "p10x":p10[0], "p10y":p10[1], "p11x":p11[0], "p11y":p11[1], \
               "p12x":p12[0], "p12y":p12[1], "p13x":p13[0], "p13y":p13[1]}

        replaceTemplates(src,dst, rep)
        of.createBlockMesh(casePath, output=False)


meshModifers={"disp2":TwoParameterDisplacement(casePath, resourcesPath), "disp4":FourParmaeterDisplacement(casePath, resourcesPath), "rebuild2":ChangeRadiusKeepTangent(casePath, resourcesPath)}

iterations =[]
pictures="/home/wojtek/Documents/studia-doktoranckie/myccfd-courses/figures/python_inst05/optianimation"
def update(params, *args):
    of.clearResults(casePath)
    objective = None

    try:
        modifer = meshModifers["".join(args)]
    except Exception:
        print "Valid methods are:", meshModifers.keys()
        exit(1)

    if len(iterations) == 0:
        modifer.init()

    modifer.modify(params)

    of.runCase(casePath, output=False)

    inletPtotalIntegral = read_last_data(totalPressureInletValues)
    outletPtotalIntegral = read_last_data(totalPressureOutletValues)

    #objective = inletPtotalIntegral - outletPtotalIntegral
    try:
        objective = inletPtotalIntegral - outletPtotalIntegral
    except Exception:
        objective = float("inf")

    iterations.append(objective)

    # of.saveCurrentImage(os.path.join(pictures,str(len(iterations))+".png"), case, colorby="total(p)")#"U"
    of.view(casePath, colorby="total(p)")

    print "Objective:",objective
    return objective


# result = optimize.fmin(update, [0.1, 0.2, 0.1, 0.2], args="disp2")
result = optimize.minimize(update, [0.1, 0.2, 0.1, 0.2], args="disp4", method="Nelder-Mead")


plt.figure()
plt.plot(iterations)
plt.title("Inlet-outlet total pressure integral difference")
plt.xlabel("Iteration No")
plt.ylabel("Objective function")
plt.grid(True)
plt.show()


# of.parview(casePath)


