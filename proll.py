import numpy as np
import pypianoroll as ppr
from pypianoroll import Multitrack, Track
from glob import glob
import matplotlib.pyplot as plt

from pychord import Chord, note_to_chord, ChordProgression

INT_TO_NOTE = np.array([
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    'F#',
    'G',
    'G#',
    'A',
    'A#',
    'B'
])

NOTE_TO_INT = {
    'Cb': 11,
    'C': 0,
    'C#': 1,
    'Db': 1,
    'D': 2,
    'D#': 3,
    'Eb': 3,
    'E': 4,
    'E#': 5,
    'Fb': 4,
    'F': 5,
    'F#': 6,
    'Gb': 6,
    'G': 7,
    'G#': 8,
    'Ab': 8,
    'A': 9,
    'A#': 10,
    'Bb': 10,
    'B': 11,
    'B#': 0
}


def main():
    # JAZZ
    # MIDI_FILES_PATH_GLOB = "../datasets/Jazz Midi/*.mid"
    # OUTFILE_PATH = "../datasets/jazz_progressions.txt"

    # Other Piano
    MIDI_FILES_PATH_GLOB = "../datasets/maestro-v2.0.0/2004/*.midi"
    OUTFILE_PATH = "../datasets/maestro_progressions.txt"

    # files = glob(MIDI_FILES_PATH_GLOB)
    write_chord_progressions_to_file(OUTFILE_PATH, MIDI_FILES_PATH_GLOB)


def get_chord_progression_from_file(f_name, debug=False):
    """
    Takes a file name returns a chord progression

    :return ChordProgression
    """

    if debug:
        print("processing: {}".format(f_name))
    mlt = Multitrack()
    try:
        mlt.parse_midi(filename=f_name, binarized=True)
        merged_mlt = mlt.get_merged_pianoroll(mode='max')
    except:
        print("unable to parse. skipping: {}".format(f_name))
        return ChordProgression()  # empty progression

    chord_progression = ChordProgression([])
    last_chord_change = 0
    for i, x in enumerate(merged_mlt):
        # print(x)
        notes = np.where(x)
        num_notes = np.sum(x)
        if num_notes:
            if num_notes > 1:
                chord_notes = INT_TO_NOTE[notes[0] % 12]
                chord_name = note_to_chord(chord_notes.tolist())
                if chord_name:
                    chord = chord_name[0]
                    if len(chord_progression.chords) == 0 or chord_progression.chords[-1] != chord:
                        # print("chord: ", notes[0], chord_notes, chord_name)
                        chord_progression.append(chord)
            # else:
            #     print("note: ", notes[0])
    # print(chord_progression)
    return chord_progression


def write_chord_progressions_to_file(output_file_path, input_files_glob):
    files = glob(input_files_glob)
    with open(output_file_path, "w") as outfile:
        for f in files:
            cp = get_chord_progression_from_file(f, debug=True)
            chord_strs = [str(c) for c in cp.chords]
            print(chord_strs)
            outfile.write(' '.join(chord_strs) + '\n')


if __name__ == '__main__':
    main()
