"""

.. _ref_example_bandgap:

Example of finding the bandgap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bandgap of a calculation can be found by:

.. code-block::
   :caption: General Format

   pyprocar.bandgap(procar="PROCAR", outcar="OUTCAR", code="vasp")


NOTE:
The bandgap calculation should be done for non-self consistent (band structure) calculations. 

.. code-block::
   :caption: Downloading example

    data_dir = pyprocar.download_example(save_dir='', 
                                material='Fe',
                                code='vasp', 
                                spin_calc_type='non-spin-polarized',
                                calc_type='bands')
"""
# sphinx_gallery_thumbnail_number = 1


###############################################################################
# importing pyprocar and specifying local data_dir

import os
import numpy as np
import pyprocar

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
data_dir = f"{parent_dir}{os.sep}data{os.sep}vasp{os.sep}non-spin-polarized{os.sep}Fe{os.sep}bands"
procar = f"{data_dir}{os.sep}PROCAR"
outcar = f"{data_dir}{os.sep}OUTCAR"


band_gap = pyprocar.bandgap(procar=procar, outcar=outcar, code="vasp")
