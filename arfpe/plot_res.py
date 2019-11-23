import scipy.special as ssp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from mpl_toolkits.axisartist.axislines import SubplotZero
matplotlib.rcParams['text.usetex'] = True

def plot_erfc_func():
    fig = plt.figure(figsize=(6, 5), facecolor='w', edgecolor='black')
    x = np.linspace(-3, 3, 64)
    # ax = SubplotZero(fig, 111)
    # fig.add_subplot(ax)
    # for direction in ["xzero", "yzero"]:
    #     # adds arrows at the ends of each axis
    #     ax.axis[direction].set_axisline_style("->")
    #
    #     # adds X and Y-axis from the origin
    #     ax.axis[direction].set_visible(True)
    #
    # for direction in ["left", "right", "bottom", "top"]:
    #     # hides borders
    #     ax.axis[direction].set_visible(False)
    # ax.axis["yzero"].set_visible(True)
    # plt.rcParams['axes.facecolor'] = 'white'
    # plt.rcParams['axes.edgecolor'] = 'white'
    #
    # plt.rcParams['grid.alpha'] = 1
    # plt.rcParams['grid.color'] = "#cccccc"
    # plt.yticks(np.arange(0.0, 2.25, 1),['0','1','2'],fontsize=32)
    # plt.ylim((-0.25, 2.25))
    plt.rc('grid', linestyle="-", color='black')
    plt.grid(True)
    plt.xlim((-3, 3))
    plt.plot(x, ssp.erfc(x), color="red", linewidth = 3, label="erfc",zorder=3)
    plt.plot([-3,3], [1,1], color="black", linewidth = 2,zorder=3)
    plt.plot([0,0], [-0.2,2.1], color="black", linewidth = 2,zorder=3)
    plt.ylim((-0.2,2.1))
    plt.ylabel("erfc(x)",size=18)
    plt.xlabel("x",size=18)
    # plt.legend(loc="best")
    plt.savefig("papergraph/erfc_example.eps", format="eps")
    plt.show()


plot_erfc_func()