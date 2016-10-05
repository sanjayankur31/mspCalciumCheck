#!/usr/bin/env python
"""
Generate a firing rate vs calcium contration.

File: calciumcheck.py

Copyright 2016 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import print_function
import nest
import numpy

points = []

for current in numpy.arange(0, 901, 5, dtype=float):
    nest.ResetKernel()
    neuron_dict = {'V_m': -60.,
                   't_ref': 5.0, 'V_reset': -60.,
                   'V_th': -50., 'C_m': 200.,
                   'E_L': -60., 'g_L': 10.,
                   'E_ex': 0., 'E_in': -80.,
                   'tau_syn_ex': 5., 'tau_syn_in': 10.,
                   'I_e': current
                   }
    nest.SetDefaults('iaf_cond_alpha', neuron_dict)

    neuron = nest.Create('iaf_cond_alpha', 1)
    detector = nest.Create('spike_detector')
    nest.Connect(neuron, detector)

    nest.Simulate(10000)
    rate = nest.GetStatus(detector, "n_events")[0] / 10.
    calcium_conc = nest.GetStatus(neuron, 'Ca')[0]
    points.append([current, rate, calcium_conc])

with open("calcium-data.txt", 'w') as outputfile:
    for point in points:
        print("{}\t{}\t{}".format(point[0], point[1], point[2]),
              file=outputfile)
