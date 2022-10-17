import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

file_name = "./Lily of the Valley.wav"# Load in audio file
buffer, sample_rate = librosa.load(file_name)
max = buffer.max()

# Get duration of audio file
duration = librosa.get_duration(y=buffer, sr=sample_rate)

librosa.display.waveshow(buffer, sr=sample_rate)
plt.savefig("out.png")
plt.show()