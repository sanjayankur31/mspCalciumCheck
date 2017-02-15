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
all_rates = []
maxval = 0.

for rate in numpy.arange(5, 50, 5, dtype=float):
    nest.ResetKernel()
    poissonExtDict = {'rate': rate, 'origin': 0., 'start': 0.}
    neuron_dict = {'beta_Ca': 0.001, 'tau_Ca': 10000.0}
    nest.SetDefaults('parrot_neuron', neuron_dict)

    neuron = nest.Create('parrot_neuron', 1)
    stim = nest.Create('poisson_generator', 1,
                       params=poissonExtDict)

    nest.Connect(stim, neuron,
                 syn_spec={'model': 'static_synapse'})

    times = []
    calc = []

    for steps in numpy.arange(0, 100 * 1000):
        nest.Simulate(1)
        calcium_conc = nest.GetStatus(neuron, 'Ca')[0]
        times.append(nest.GetKernelStatus()['time'])
        calc.append(calcium_conc)
        points.append([nest.GetKernelStatus()['time'], calcium_conc])

    all_times.append(times)
    all_calcs.append(calc)
    all_rates.append("{}Hz".format(rate))

    with open("calcium-data-{}Hz.txt".format(rate), 'w') as outputfile:
        for point in points:
            print("{}\t{}".format(point[0], point[1]),
                  file=outputfile)

    maxval = numpy.amax(calc[4000:5000])
    minval = numpy.amin(calc[4000:5000])
    rescaled_cal = [(((i - minval) * 10)/(maxval - minval) - 60) for i in calc]

    fig = plt.figure(figsize=(40, 10))
    axes = plt.gca()
    # axes.set_ylim([0, 120])
    plt.xlabel('time (ms)')
    plt.title('Ca conc with {} Hz poisson stim'.format(rate))
    plt.plot(times[4000:5000], rescaled_cal[4000:5000],
             label="([Ca2+] interval rescaled to [0,10], translated to x=-60")
    plt.legend()
    plt.savefig("parrot-calcium-vanilla-data-{}Hz.png".format(rate))
    plt.close(fig)

fig2 = plt.figure(figsize=(40, 10))
axes = plt.gca()
# axes.set_ylim([0, 1.2])
plt.xlabel('time (ms)')
plt.ylabel('calcium concentration')
plt.title('Ca conc with different input poisson stim')
lines = []
for i in range(0, len(all_times)):
    line = plt.plot(all_times[i], all_calcs[i], label=all_rates[i])
    plt.axhline(y=numpy.mean(all_calcs[i]), color=line[0].get_color())
    lines = lines + line
plt.legend(handles=lines, loc='upper left')
plt.savefig("parrot-calcium-vanilla-data-combined.png".format(rate))
plt.close(fig2)
