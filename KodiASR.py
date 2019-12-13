from control import Control
import pyaudio
import wave
from websocket import create_connection
import json
import sys

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 8000  # Record at 44100 samples per second
seconds = 3
filename = "test.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

inf = "test.wav"
if len(sys.argv) > 1:
    inf = sys.argv[1]

def process_chunk(ws, buf):
    ws.send_binary(buf)
    res = ws.recv()
    # print(res)

def process_final_chunk(ws):
    a = Control()
    ws.send('{"eof" : 1}')
    res = ws.recv()
    print(res)
    res = json.loads(res)
    res = res["result"]
    for item in res:
        print(item["word"])
        try:
            a.dispatcher(item["word"])
            break
        except Exception as e:
            print(e)
            continue
    
    ws.close()

def test_stream():
    ws = create_connection("wss://api.alphacephei.com/asr/en/")

    infile = open(inf, "rb")

    while True:
        buf = infile.read(8000)
        if not buf:
            break
        process_chunk(ws, buf)

    process_final_chunk(ws)

test_stream()
