import subprocess, os

OF_DIR ="/opt/openfoam231"
PARAVIEW ="/home/wgryglas/Applications/ParaView-4.3.1-Linux-64bit/bin/paraview"



def runBashCommands(cwd, *args):
    command = "; ".join(args)
    process = subprocess.Popen(command, cwd=cwd, executable="/bin/bash", shell=True, stdout=subprocess.PIPE)
    print process.communicate()[0]


def runCase(casePath, openfoamDir=None):
    if not openfoamDir:
        openfoamDir = OF_DIR
    bashrc = os.path.join(openfoamDir, "etc", "bashrc")
    runBashCommands(casePath, "source "+bashrc, "simpleFoam")


def clearCase(casePath, openfoamDir=None):
    if not openfoamDir:
        openfoamDir = OF_DIR
    clearFunctioinsFile = os.path.join(openfoamDir, "bin","tools","CleanFunctions")
    runBashCommands(casePath, "source "+clearFunctioinsFile, "cleanCase")


def clearResults(casePath, openfoamDir=None):
    if not openfoamDir:
        openfoamDir = OF_DIR
    clearFunctioinsFile = os.path.join(openfoamDir, "bin","tools","CleanFunctions")
    runBashCommands(casePath, "source "+clearFunctioinsFile, "cleanTimeDirectories", "rm -r postProcessing")


def createBlockMesh(casePath, openfoamDir=None):
    if not openfoamDir:
        openfoamDir = OF_DIR
    bashrc = os.path.join(openfoamDir, "etc", "bashrc")
    runBashCommands(casePath, "source "+bashrc, "blockMesh")


def __createStateFile__(casePath):
    name = os.path.basename(casePath)
    name += ".foam"
    toReplacePath="FOAM_FILE"
    post = os.path.join(casePath, name)

    toReplaceName = "FOAM_NAME"

    open(os.path.join(casePath,name),"w").close()

    state=os.path.join(casePath,"postprocessing.pvsm")
    state2=os.path.join(casePath,"postprocessing2.pvsm")

    lines =[]
    changed=False
    with open(state, "r") as f:
        for l in f:
            if toReplacePath in l:
                l = l.replace(toReplacePath, post)
                changed=True

            if toReplaceName in l:
                l = l.replace(toReplaceName, name)
                changed=True

            lines.append(l)

    if not changed:
        return

    print "writing state file..."

    with open(state2,"w") as f2:
        f2.writelines(lines)

    os.remove(state)
    os.rename(state2, state)


def view(casePath, paraview=None):
    if not paraview:
        paraview = PARAVIEW
    __createStateFile__(casePath)
    state=os.path.join(casePath,"postprocessing.pvsm")
    runBashCommands(casePath, paraview+" --state="+state)

    # name = os.path.basename(casePath)
    # name += ".foam"
    # runBashCommands(casePath, paraview+" "+name)


def hasMesh(case):
    polyMesh = os.path.join(case, "constant", "polyMesh")
    required = ["points", "boundary", "faces", "owner", "neighbour"]
    for f in os.listdir(polyMesh):
        if f in required:
            required.remove(f)

    return len(required) == 0
