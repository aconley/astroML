from __future__ import print_function

import os

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import numpy as np

from .tools import get_data_home

# Info on vega spectrum: http://www.stsci.edu/hst/observatory/cdbs/calspec.html
VEGA_URL = 'ftp://ftp.stsci.edu/cdbs/current_calspec/ascii_files/1732526_nic_002.ascii'
FILTER_URL = 'http://www.sdss.org/dr7/instruments/imager/filters/%s.dat'


def fetch_sdss_filter(fname, data_home=None, download_if_missing=True):
    """Loader for SDSS Filter profiles

    Parameters
    ----------
    fname : str
        filter name: must be one of 'ugriz'
    data_home : optional, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit learn data is stored in '~/astroML_data' subfolders.

    download_if_missing : optional, default=True
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------
    data : ndarray
        data is an array of shape (5, Nlam)
        first row: wavelength in angstroms
        second row: sensitivity to point source, airmass 1.3
        third row: sensitivity to extended source, airmass 1.3
        fourth row: sensitivity to extended source, airmass 0.0
        fifth row: assumed atmospheric extinction, airmass 1.0
    """
    if fname not in 'ugriz':
        raise ValueError("Unrecognized filter name '%s'" % fname)
    url = FILTER_URL % fname

    data_home = get_data_home(data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)

    archive_file = os.path.join(data_home, '%s.dat' % fname)

    if not os.path.exists(archive_file):
        if not download_if_missing:
            raise IOError('data not present on disk. '
                          'set download_if_missing=True to download')

        print("downloading from %s" % url)
        F = urlopen(url)
        dat = F.read()
        F.close()
        outf = open(archive_file, 'w')
        try:
            # Python 2.x
            outf.write(dat)
        except TypeError:
            outf.write(dat.decode())
            
        outf.close()

    F = open(archive_file)

    return np.loadtxt(F, unpack=True)


def fetch_vega_spectrum(data_home=None, download_if_missing=True):
    """Loader for Vega reference spectrum

    Parameters
    ----------
    fname : str
        filter name: must be one of 'ugriz'
    data_home : optional, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit learn data is stored in '~/astroML_data' subfolders.

    download_if_missing : optional, default=True
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------
    data : ndarray
        data[0] is the array of wavelength in angstroms
        data[1] is the array of fluxes in Jy (F_nu, not F_lambda)
    """
    data_home = get_data_home(data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)

    archive_name = os.path.join(data_home, VEGA_URL.split('/')[-1])

    if not os.path.exists(archive_name):
        if not download_if_missing:
            raise IOError('data not present on disk. '
                          'set download_if_missing=True to download')

        print("downnloading from %s" % VEGA_URL)
        F = urlopen(VEGA_URL)
        dat = F.read()
        F.close()
        outf = open(archive_name, 'w')
        try:
            # Python 2.x
            outf.write(F.read())
        except TypeError:
            outf.write(F.read())

        outf.close()

    F = open(archive_name)

    return np.loadtxt(F, unpack=True)
