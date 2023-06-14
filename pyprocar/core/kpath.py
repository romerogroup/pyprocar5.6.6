# -*- coding: utf-8 -*-


import numpy as np
import pyvista
from ..utils import mathematics


class KPath:
    def __init__(
        self, knames=None, special_kpoints=None, ngrids=None, has_time_reversal=True,
    ):
        latex = "$"
        for x in knames:
            if "$" in x[0] or "$" in x[1]:
                latex = ""
        self.knames = [[latex + x[0] + latex, latex + x[1] + latex] for x in knames]
        self.special_kpoints = special_kpoints
        self.ngrids = ngrids
        self.has_time_reversal = has_time_reversal

    @property
    def nsegments(self):
        return len(self.knames)

    @property
    def tick_positions(self):
        pos = 0
        tick_positions = [pos]
        for isegment in range(self.nsegments):
            pos += self.ngrids[isegment]
            tick_positions.append(pos - 1)
        return tick_positions

    @property
    def tick_names(self):
        tick_names = [self.knames[0][0], self.knames[0][1]]
        if len(self.knames) == 1:
            return tick_names
        for isegment in range(1, self.nsegments):
            if self.knames[isegment][0] != self.knames[isegment-1][1]:
                tick_names[-1] += "|" + self.knames[isegment][0]
            tick_names.append(self.knames[isegment][1])
        return tick_names

    @property
    def kdistances(self):
        distances = []
        for isegment in range(self.nsegments):
            distances.append(
                np.linalg.norm(
                    self.special_kpoints[isegment][0]
                    - self.special_kpoints[isegment][1]
                )
            )
        return np.array(distances)

    def get_optimized_kpoints_transformed(
        self, transformation_matrix, same_grid_size=False
    ):
        """

        Parameters
        ----------
        transformation_matrix : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        new_special_kpoints = np.dot(self.special_kpoints, transformation_matrix)
        new_ngrids = self.ngrids.copy()
        for isegment in range(self.nsegments):
            kstart = new_special_kpoints[isegment][0]
            kend = new_special_kpoints[isegment][1]
            kpoints_old = np.linspace(
                self.special_kpoints[isegment][0],
                self.special_kpoints[isegment][1],
                self.ngrids[isegment],
            )

            dk_vector_old = kpoints_old[-1] - kpoints_old[-2]
            dk_old = np.linalg.norm(dk_vector_old)

            # this part is to find the direction
            distance = kend - kstart

            # this part is to find the high symmetry points on the path
            expand = (np.linspace(kstart, kend, 1000) * 2).round(0) / 2

            unique_indexes = np.sort(np.unique(expand, return_index=True, axis=0)[1])
            symm_kpoints_path = expand[unique_indexes]

            # this part is to only select poits that are after kstart and not before

            angles = np.array(
                [
                    mathematics.get_angle(x, distance, radians=False)
                    for x in (symm_kpoints_path - kstart)
                ]
            ).round()
            symm_kpoints_path = symm_kpoints_path[angles == 0]
            if len(symm_kpoints_path) < 2:
                continue
            suggested_kstart = symm_kpoints_path[0]
            suggested_kend = symm_kpoints_path[1]

            if np.linalg.norm(distance) > np.linalg.norm(
                suggested_kend - suggested_kstart
            ):
                new_special_kpoints[isegment][0] = suggested_kstart
                new_special_kpoints[isegment][1] = suggested_kend

            # this part is to get the number of gird points in the to have the
            # same spacing is before the transformation
            if same_grid_size:
                new_ngrids[isegment] = int(
                    (
                        np.linalg.norm(
                            new_special_kpoints[isegment][0]
                            - new_special_kpoints[isegment][1]
                        )
                        / dk_old
                    ).round(4)
                    + 1
                )
        return KPath(
            knames=self.knames, special_kpoints=new_special_kpoints, ngrids=new_ngrids
        )

    def get_kpoints_transformed(
        self, transformation_matrix,
    ):
        new_special_kpoints = np.dot(self.special_kpoints, transformation_matrix)
        return KPath(
            knames=self.knames, special_kpoints=new_special_kpoints, ngrids=self.ngrids
        )

    def write_to_file(self, filename="KPOINTS", fmt="vasp"):
        wf = open(filename, "w")
        if fmt == "vasp":
            wf.write("! Generated by pyprocar\n")
            if len(np.unique(self.ngrids)) == 1:
                wf.write(str(self.ngrids[0]) + "\n")
            else:
                wf.write("   ".join([str(x) for x in self.ngrids]) + "\n")
            wf.write("Line-mode\n")
            wf.write("reciprocal\n")
            for isegment in range(self.nsegments):
                wf.write(
                    " ".join(
                        [
                            "  {:8.4f}".format(x)
                            for x in self.special_kpoints[isegment][0]
                        ]
                    )
                    + "   ! "
                    + self.knames[isegment][0].replace("$", "")
                    + "\n"
                )
                wf.write(
                    " ".join(
                        [
                            "  {:8.4f}".format(x)
                            for x in self.special_kpoints[isegment][1]
                        ]
                    )
                    + "   ! "
                    + self.knames[isegment][1].replace("$", "")
                    + "\n"
                )
                wf.write("\n")
        wf.close()
