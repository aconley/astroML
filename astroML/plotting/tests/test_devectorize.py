import matplotlib
matplotlib.use('Agg')  # don't display plots

import numpy as np
from numpy.testing import assert_
from matplotlib import image
import matplotlib.pyplot as plt

try:
    # Python 2.x
    from cStringIO import StringIO as ioObj
except ImportError:
    # Python 3.x
    from io import BytesIO as ioObj

from astroML.plotting.tools import devectorize_axes


def test_devectorize_axes():
    np.random.seed(0)

    x, y = np.random.random((2, 1000))

    # save vectorized version
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    sio = ioObj()
    fig.savefig(sio)
    sio.seek(0, 0)  # Go back to start
    im1 = image.imread(sio)
    plt.close()

    # save devectorized version
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    devectorize_axes(ax, dpi=200)
    sio = ioObj()
    fig.savefig(sio)
    sio.seek(0, 0)
    im2 = image.imread(sio)
    plt.close()

    assert_(im1.shape == im2.shape)
    assert_((im1 != im2).sum() < 0.1 * im1.size)
