import subprocess, os

__OF_DEFAULT_DIR__="/opt/openfoam231"
__PARAVIEW_DEFAULT_DIR__="/home/wgryglas/Applications/ParaView-4.3.1-Linux-64bit/bin/paraview"

def runBashCommands(cwd, *args):
    command = "; ".join(args)
    process = subprocess.Popen(command, cwd=cwd, executable="/bin/bash", shell=True, stdout=subprocess.PIPE)
    print process.communicate()[0]

def runCase(casePath, openfoamDir=__OF_DEFAULT_DIR__):
    bashrc = os.path.join(openfoamDir, "etc", "bashrc")
    runBashCommands(casePath, "source "+bashrc, "simpleFoam")

def clearCase(casePath, openfoamDir=__OF_DEFAULT_DIR__):
    clearFunctioinsFile = os.path.join(openfoamDir, "bin","tools","CleanFunctions")
    runBashCommands(casePath, "source "+clearFunctioinsFile, "cleanCase")

def clearResults(casePath, openfoamDir=__OF_DEFAULT_DIR__):
    clearFunctioinsFile = os.path.join(openfoamDir, "bin","tools","CleanFunctions")
    runBashCommands(casePath, "source "+clearFunctioinsFile, "cleanTimeDirectories", "rm -r postProcessing")

def createBlockMesh(casePath, openfoamDir=__OF_DEFAULT_DIR__):
    bashrc = os.path.join(openfoamDir, "etc", "bashrc")
    runBashCommands(casePath, "source "+bashrc, "blockMesh")

def view(casePath, paraview=__PARAVIEW_DEFAULT_DIR__):
    state=os.path.join(casePath,"postprocessing.pvsm")
    runBashCommands(casePath, paraview+" --state="+state)


def hasMesh(case):
    polyMesh = os.path.join(case, "constant", "polyMesh")
    required = ["points", "boundary", "faces", "owner", "neighbour"]
    for f in os.listdir(polyMesh):
        if f in required:
            required.remove(f)

    return len(required) == 0



def setup(of_dir, paraview_bin_dir, stateFileName="postprocessing.pvsm"):
    __OF_DEFAULT_DIR__ = of_dir
    __PARAVIEW_DEFAULT_DIR__ = paraview_bin_dir