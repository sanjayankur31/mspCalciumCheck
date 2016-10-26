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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nest
import numpy

points = []
all_times = []
all_calcs = []
all_currents = []

for current in numpy.arange(0, 901, 50, dtype=float):
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

    times = []
    calc = []

    for steps in numpy.arange(0, 50000):
        nest.Simulate(1)
        calcium_conc = nest.GetStatus(neuron, 'Ca')[0]
        times.append(nest.GetKernelStatus()['time'])
        calc.append(calcium_conc)
        points.append([nest.GetKernelStatus()['time'], calcium_conc])

    nest.SetStatus(neuron, {'I_e': 0.})
    for steps in numpy.arange(0, 50000):
        nest.Simulate(1)
        calcium_conc = nest.GetStatus(neuron, 'Ca')[0]
        times.append(nest.GetKernelStatus()['time'])
        calc.append(calcium_conc)
        points.append([nest.GetKernelStatus()['time'], calcium_conc])

    all_times.append(times)
    all_calcs.append(calc)
    all_currents.append("{}pA".format(current))

    with open("calcium-data-{}pA.txt".format(current), 'w') as outputfile:
        for point in points:
            print("{}\t{}".format(point[0], point[1]),
                  file=outputfile)

    fig = plt.figure(figsize=(15,10))
    axes = plt.gca()
    axes.set_ylim([0,1.5])
    plt.xlabel('time (ms)')
    plt.ylabel('calcium concentration')
    plt.title('Calcium concentration with {} pA constant current'.format(current))
    plt.axvline(x=50000)
    plt.plot(times, calc)
    plt.savefig("calcium-data-{}pA.png".format(current))
    plt.close(fig)

fig2 = plt.figure(figsize=(15,10))
axes = plt.gca()
axes.set_ylim([0,1.5])
plt.xlabel('time (ms)')
plt.ylabel('calcium concentration')
plt.title('Calcium concentration with different pA constant current'.format(current))
plt.axvline(x=50000)
for i in range(0, len(all_times)):
    plt.plot(all_times[i], all_calcs[i])
plt.legend(all_currents, loc='upper left')
plt.savefig("calcium-data-combined.png".format(current))
plt.close(fig2)
