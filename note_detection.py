#!/usr/bin/env python
"""
note_detection.py

Copyright (c) Weipeng He <weipeng.he@idiap.ch>
"""

import math
import sounddevice as sd
import numpy as np
import Gnuplot


_STANDARD_PITCH = 440.0
_NOTE_NAMES = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


def _find_nonzero_peak(y):
    h = -1.0
    p = 0
    for i in xrange(1, len(y) - 1):
        if y[i] > h and y[i] >= y[i-1] and y[i] >= y[i+1]:
            h = y[i]
            p = i
    return p


def _hertz_to_note(hertz):
    value = math.log(hertz / _STANDARD_PITCH, 2.0) * 12.0
    notei = int(round(value))
    res = value - notei
    octave = (notei + 9) // 12 + 4
    return '%02s-%d %+.0f' % (_NOTE_NAMES[notei % 12], octave, 100.0 * res)


class NoteDetector:
    def __init__(self):
        self.fs = 44100
        self.stream = sd.InputStream(samplerate=self.fs, blocksize=4096,
                                     channels=1, callback=self.detect)
        self.gplot = Gnuplot.Gnuplot()
        self.gplot('set yrange [-1:1]')

    def detect(self, indata, frames, time, status):
        sig = indata[:, 0]
        nfft = len(sig)
        sig = sig * np.hamming(nfft)
        dft = np.fft.fft(sig)
        acr = np.fft.ifft(dft * dft.conj()).real[:nfft/2]
        acrn = acr / (acr[0] + 1e-2)
        self.gplot.plot(Gnuplot.Data(acrn, with_='l'))
        pindex = _find_nonzero_peak(acr)
        if pindex > 0:
            pitch = 1.0 / pindex * self.fs
            print '%s (%.1fHz)' % (_hertz_to_note(pitch), pitch)
        else:
            print 'unknown'

    def start(self):
        self.stream.start()

    def close(self):
        self.stream.close()


def main():
    nd = NoteDetector()
    nd.start()
    raw_input('Press "Enter" to stop')
    nd.close()


if __name__ == "__main__":
    main()


# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
