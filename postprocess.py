import cmath
import matplotlib.pyplot as plt
import os
from os.path import split as pathsplit
from os.path import join as pathjoin
import numpy as np
from numpy import abs as mag, angle
from PyLTSpice import RawRead


def what_to_units(whattype):
    """Determines the unit to display on the plot Y axis"""
    if 'voltage' in whattype:
        return 'V'
    if 'current' in whattype:
        return 'A'

def convert_to_dB(value):
    return 20*np.log10(abs(value))

def convert_to_phase(value):
    return np.angle(value, deg=True)

directory = os.getcwd()
test_directory = './test'
filename = 'MultiCapModel.raw'
raw_filename = pathjoin(test_directory, filename)

LTR = RawRead(raw_filename, verbose=True)

voltage_trace = LTR.get_trace("V(n001)")
current_trace = LTR.get_trace("I(V1)")

impedance_data = voltage_trace / np.where(current_trace.data != 0, current_trace.data, 1)

gain = convert_to_dB(impedance_data)
phase = convert_to_phase(impedance_data)

x_data = LTR.get_trace(voltage_trace.name).axis

fig,ax1 = plt.subplots(figsize=(10, 6))

# Plot magnitude on primary axis
color = 'tab:red'
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Impedance Magnitude [dB]', color=color)
ax1.plot(x_data, gain, color=color, label="Magnitude (dB)")
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xscale('log')

# Create secondary axis for phase
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Phase [degrees]', color=color)
ax2.plot(x_data, phase, color=color, linestyle='--', label="Phase (degrees)")
ax2.tick_params(axis='y', labelcolor=color)

# Title and show plot
plt.title("Impedance Magnitude and Phase of V(n001)/I(V1)")
fig.tight_layout()
plt.show()