import numpy as np
from pypianoroll import Multitrack, Track
from matplotlib import pyplot as plt

# Create a pianoroll matrix, where the first and second axes represent time
# and pitch, respectively, and assign a C major chord to the pianoroll
pianoroll = np.zeros((96, 128))
C_maj = [60, 64, 67, 72, 76, 79, 84]
pianoroll[0:95, C_maj] = 100

# Create a `pypianoroll.Track` instance
track = Track(pianoroll=pianoroll, program=0, is_drum=False,
              name='my awesome piano')

# Plot the pianoroll
fig, ax = track.plot()
plt.show()
