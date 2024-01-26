#!/usr/bin/env python

import math
import numpy as np
from gnuradio import gr

class fsk_modulator(gr.interp_block):
    def __init__(self, baud_rate=48e2, interpolation=10, freq_deviation=12e2, endian='big'):  # only default arguments here

        gr.interp_block.__init__(
            self,
            name='FSK Modulator',   # will show up in GRC
            in_sig=[np.uint8],       # input byte
            out_sig=[np.complex64],  # output complex value 2 x 32-bits floats
            interp = 8*interpolation
        )
        # if an attribute with the same name as a parameter is found, a callback is registered (properties work, too).
        self.baud_rate = baud_rate
        self.freq_deviation = freq_deviation

        self.samp_rate = baud_rate * interpolation
        self.sensitivity = (2.0 * math.pi * freq_deviation / 1.0)
        self.sensitivity_per_sample = self.sensitivity / self.samp_rate
        
        self.interpolation = interpolation
        self.endian = endian # 'big' (from MSB to LSB) or 'little' (from LSB to MSB)
        self.set_relative_rate(8*interpolation) # setting of output samples to input samples ratio, 8 is number of bits in byte

        self.phase_accumulator = 0

    def work(self, input_items, output_items):
        bits_unpacked = np.unpackbits(input_items, bitorder = self.endian)
        bits_repeated = np.repeat(bits_unpacked, self.interpolation) # interpolation
        bits_output = bits_repeated
        
        phase_addition = bits_output * self.sensitivity_per_sample
        phase_cumulative = (np.cumsum(phase_addition) + self.phase_accumulator) % (2*math.pi)
        self.phase_accumulator = phase_cumulative[-1]

        signal_inphase = np.cos(phase_cumulative)
        signal_quadrature = np.sin(phase_cumulative)
        signal_complex = signal_inphase + 1j * signal_quadrature

        output_items[0][:] = signal_complex
        
        return len(output_items[0])

