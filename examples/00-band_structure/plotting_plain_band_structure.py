"""

.. _ref_plotting_plain_band_structure:

Plotting plain band structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Plotting plain band structure .


"""

import os
import pyprocar


data_dir = f'C:{os.sep}Users{os.sep}lllang{os.sep}Desktop{os.sep}Romero Group Research{os.sep}Research Projects{os.sep}pyprocar2{os.sep}data{os.sep}qe{os.sep}bands{os.sep}colinear{os.sep}Fe'


pyprocar.bandsplot(
                code='qe', 
                mode='plain',
                dirname=data_dir)