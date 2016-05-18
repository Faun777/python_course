
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
    pass


#TEST (Waring below lines should be commented out when this module will be used in other files)
import numpy as np
X, Y = np.meshgrid(np.linspace(0,1,100), np.linspace(0,1,100))

Z = []
for t in np.linspace(0, 2*np.pi, 50):
    Z.append( np.exp(2*X*Y)*np.sin(t) )

animate_contour_plot(Z, dataRange=(-10.,10.))