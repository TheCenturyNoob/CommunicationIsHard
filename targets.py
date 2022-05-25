import pyaudio


class Target:
    p = pyaudio.PyAudio()

    def __init__(self, audioformat, channels, framerate):
        self.stream = None
        self.audioformat = audioformat
        self.channels = channels
        self.framerate = framerate

    def get_stream(self):
        self.stream = self.p.open(format=self.audioformat, channels=self.channels, rate=self.framerate, output=True)
        self.stream.start_stream()
        return self.stream

    def close(self):
        self.stream.stop_stream()
        self.stream.close()