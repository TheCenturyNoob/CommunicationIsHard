"""PyAudio Example: Play a wave file (callback version)."""

import time
from io import BytesIO

import pyaudio

from sources import MicSource, FileSource
from targets import Target

p = pyaudio.PyAudio()
audioformat = pyaudio.paInt32
ch = 2
rate = 44100

# source = MicSource(audioformat, ch, rate, 3)
source = FileSource(1)
target = Target(source.audioformat, source.channels, source.framerate)

target_stream = target.get_stream()
source_stream = source.get_stream(target_stream)

while source_stream.is_active():
    time.sleep(0.1)

target.close()
source.close()
p.terminate()