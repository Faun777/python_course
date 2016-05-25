
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

    if len(framesDatas)==0:
        raise Exception("Data frames number should be at least one")


    Nx,Ny = framesDatas[0].shape

    X, Y = np.meshgrid(np.linspace(sizeX[0], sizeX[1], Nx), np.linspace(sizeY[0], sizeY[1], Ny))

    if not dataRange:
        minD = min(framesDatas[0].flatten())
        maxD = max(framesDatas[0].flatten())
    else:
        minD,maxD = dataRange

    fig = plt.figure()
    plt.axes().set_aspect('equal', 'datalim')
    cs = plt.contourf(X, Y, framesDatas[0], nLevels)
    fig.colorbar(cs, ticks=np.linspace(minD, maxD, nLevels+1))

    if len(framesDatas) > 1:
        def animate(i):
            i = i*skip
            cs=plt.contourf(X, Y, framesDatas[i], nLevels)
            cs.zmin = minD
            cs.zmmax = maxD
            plt.title('Frame %d' % (i+1))
            return cs

        anim = animation.FuncAnimation(fig, animate, frames=int(len(framesDatas)/skip) , interval=5, repeat=repeat)

    plt.show()


#TEST
# import numpy as np
# X, Y = np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))
#
# Z = []
# for t in np.linspace(0, 2*np.pi, 50):
#     Z.append( np.exp(2*X*Y)*np.sin(t) )
#
# animate_contour_plot(Z, dataRange=(-10.,10.))
