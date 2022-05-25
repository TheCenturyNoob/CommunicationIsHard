import audioop
import wave

import pyaudio


class Source:
    p = pyaudio.PyAudio()

    def __init__(self, volume):
        self.stream = None
        self.target_stream = None
        self.volume = volume

    def callback(self, in_data, frame_count, time_info, status):
        self.target_stream.write(audioop.mul(in_data, self.audioformat, self.volume))
        return in_data, pyaudio.paContinue

    def close(self):
        self.stream.stop_stream()
        self.stream.close()


class MicSource(Source):
    def __init__(self, audioformat, channels, framerate, volume):
        super().__init__(volume)
        self.audioformat = audioformat
        self.channels = channels
        self.framerate = framerate

    def get_stream(self, target_stream):
        self.target_stream = target_stream
        self.stream = self.p.open(format=self.audioformat, channels=self.channels, rate=self.framerate, input=True, stream_callback=self.callback, input_device_index=1)
        self.stream.start_stream()
        return self.stream


class FileSource(Source):
    def __init__(self, volume, socket=None):
        super().__init__(volume)
        self.socket = socket
        self.wf = wave.open('sample.wav', 'rb')
        self.audioformat = self.p.get_format_from_width(self.wf.getsampwidth())
        self.channels = self.wf.getnchannels()
        self.framerate = self.wf.getframerate()

    def get_stream(self, target_stream):
        self.target_stream = target_stream
        self.stream = self.p.open(format=self.audioformat, channels=self.channels, rate=self.framerate, input=True, stream_callback=self.callback)
        self.stream.start_stream()
        return self.stream

    def callback(self, in_data, frame_count, time_info, status):
        if self.socket:
            data = audioop.mul(self.wf.readframes(frame_count), self.audioformat, self.volume)
            print(len(data))
            self.socket.sendall(data)
        else:
            self.target_stream.write(audioop.mul(self.wf.readframes(frame_count), self.audioformat, self.volume))

        return in_data, pyaudio.paContinue