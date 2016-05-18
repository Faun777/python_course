
def animate_contour_plot(framesDatas, sizeX=(0,1), sizeY=(0,1), dataRange=None, nLevels=10, skip=1, repeat=False ):
    """
    Function which make animation from set of 2D data on cartesian grid
    :param framesDatas: List of 2D numpy.arrays containing nodal values
    :param sizeX: tuple holding domain range in X dir
    :param sizeY: tuple holding domain range in Y dir
    :param skip: number of frames to be skipped
    :param nLevels: number of color levels
    :param dataRange: tuple holding min and max value for data range to be displayed in plot and colorbar
    :return: None
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import animation
    nx, ny = framesDatas[0].shape

    Z0 = framesDatas[0]
    if dataRange:
        minVal,maxVal=dataRange
    else:
        minVal = min(Z0.flatten())
        maxVal = max(Z0.flatten())

    x = np.linspace(sizeX[0],sizeX[1],nx)
    y = np.linspace(sizeY[0],sizeY[1],ny)
    X,Y = np.meshgrid(x,y)
    fig = plt.figure()
    cs=plt.contourf(X,Y,Z0,nLevels)
    cs.zmax=maxVal
    cs.zmin=minVal
    plt.colorbar(cs,ticks=np.linspace(minVal,maxVal,nLevels+1))
    if len(framesDatas)>1:
    #     tworzymy animacje
        def animate(nFrame):
            # nFrame=nFrame*skip
            Z = framesDatas[nFrame]
            cs= plt.contourf(X,Y,Z,nLevels)
            cs.zmax=maxVal
            cs.zmin=minVal
            # plt.colorbar(cs,ticks=np.linspace(minVal,maxVal,nLevels+1))
            return cs
        anim = animation.FuncAnimation(fig,animate,frames=int(len(framesDatas)/skip),repeat=repeat)
    plt.show()

#TEST (Waring below lines should be commented out when this module will be used in other files)
import numpy as np
X, Y = np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))

Z = []
for t in np.linspace(0, 2*np.pi, 50):
    Z.append( np.exp(2*X*Y)*np.sin(t) )

animate_contour_plot(Z, nLevels=20,dataRange=(-10.,10.))