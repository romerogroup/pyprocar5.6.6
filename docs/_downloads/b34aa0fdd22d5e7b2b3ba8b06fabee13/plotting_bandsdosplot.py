"""

.. _ref_plotting_bandsdosplot:

Plotting bandsdosplot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Plotting bandsdosplot example.

First download the example files with the code below. Then replace data_dir below.

.. code-block::
   :caption: Downloading example

   bands_dir = pyprocar.download_example(save_dir='', 
                                material='Fe',
                                code='qe', 
                                spin_calc_type='non-spin-polarized',
                                calc_type='bands')

   dos_dir = pyprocar.download_example(save_dir='', 
                                material='Fe',
                                code='qe', 
                                spin_calc_type='non-spin-polarized',
                                calc_type='dos')
"""


###############################################################################
# importing pyprocar and specifying local data_dir
import os
import pyprocar


parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
bands_dir = f"{parent_dir}{os.sep}data{os.sep}qe{os.sep}bands{os.sep}colinear{os.sep}Fe"
dos_dir = f"{parent_dir}{os.sep}data{os.sep}qe{os.sep}dos{os.sep}colinear{os.sep}Fe"
###############################################################################
# Plain mode
# +++++++++++++++++++++++++++++++++++++++
# The keywords that works for bandsplot and dosplot will work in bandsdosplot. 
# These keyword arguments can be set in bands_settings and dos_settings as done below.
#

bands_settings = {'mode':'plain',
                'dirname': bands_dir}

dos_settings = {'mode':'plain',
                'dirname': dos_dir}

pyprocar.bandsdosplot(code='qe',
                bands_settings=bands_settings,
                dos_settings=dos_settings,
                )


