import fasttext
import numpy as np
import pypianoroll
from pypianoroll import Multitrack, Track
from glob import glob
import matplotlib.pyplot as plt

from pychord import Chord, note_to_chord, ChordProgression
from proll import NOTE_TO_INT
from hypercube import (
    chord_to_binary,
    bin_to_note_ints,
    get_hypercube_neighbor_path,
    get_random_outward_path
)

MODEL_OUT_PATH = './models/jazz_progressions-12d.mdl.fasttext'
# MODEL_OUT_PATH = './models/maestro_progressions-12d.mdl.fasttext'


def load_mdl(m_path):
    model = fasttext.load_model(m_path)
    random_chosen_chord_str = np.random.choice(model.words, 1)
    random_chosen_chord = Chord(random_chosen_chord_str[0][0])
    return model


def test_model(mdl):
    for word in mdl.words[0:10]:
        neighbors = mdl.get_nearest_neighbors(word)
        neighbor_chords = [n[1] for n in neighbors]
        print("chord: {}, neighbors: {}".format(word, neighbor_chords[0:10]))
    return


def generate_chord_progression(mdl, starting_chord, length, max_memory=4, random_neighbors=False):
    progression = ChordProgression(Chord(starting_chord))
    current_chord = starting_chord
    memory = []
    top_k = 10
    if max_memory > 0:
        memory = [current_chord]

    for i in range(0, length):
        next_chord = current_chord
        # print("current_chord: ", current_chord)
        neighbors = mdl.get_nearest_neighbors(next_chord, top_k)
        neighbor_chords = [n[1] for n in neighbors]
        # print("\tneighbors:", neighbor_chords)
        # choose random neighbor
        if random_neighbors:
            processed_neighbors = np.random.choice(neighbor_chords, top_k)
        else:
            processed_neighbors = neighbor_chords

        if len(processed_neighbors):
            # choose sequential neighbors
            for neighbor in processed_neighbors:
                if neighbor != next_chord and neighbor not in memory:
                    next_chord = neighbor
                    memory.append(next_chord)
                    if len(memory) >= max_memory:
                        memory.pop(0)  # remove first element

            # random_neighbors = np.random.choice(neighbor_chords, 1)
            # print("\trandom_neighbors: ", random_neighbors)
            # next_chord = random_neighbors[0]

            current_chord = next_chord
            if current_chord:
                chrd = Chord(current_chord)
                progression.append(chrd)
    return progression


def choose_random_chord(mdl):
    random_chosen_chord_str = np.random.choice(mdl.words, 1)
    # print(random_chosen_chord_str)
    random_chosen_chord = random_chosen_chord_str[0]
    return random_chosen_chord


def rand_octave_shift(max_num=1.0):
    return int((np.random.rand() * max_num))


def get_next_chord(mdl, chrd, memory_size=0, random_neighbors=False, hypercube=False):
    if not hypercube:
        prg = generate_chord_progression(
            mdl, chrd, 1, max_memory=memory_size, random_neighbors=random_neighbors)
    else:
        bin_note_ints = chord_to_binary(chrd)
        note_ints = bin_to_note_ints(bin_note_ints)
        path = get_hypercube_neighbor_path(note_ints)
        if len(path):
            return path[0]
        else:
            return None
    return prg.chords[-1]


def generate_hypercube_progression(chrd):
    bin_note_ints = chord_to_binary(chrd)
    note_ints = bin_to_note_ints(bin_note_ints)
    path = get_hypercube_neighbor_path(note_ints)
    if len(path):
        return ChordProgression(path)
    else:
        return ChordProgression([])


def generate_pianoroll_from_progression(prog, num_chords, duration):
    pianoroll = np.zeros((num_chords * duration, 128))
    # C_maj = [60, 64, 67, 72, 76, 79, 84]
    # pianoroll[0:95, C_maj] = 100
    vel = 100
    gap_size = 12
    spread = 4.0
    # def sample_notes(n): return np.random.choice(n, rand_octave_shift(3) + 1)

    def sample_notes(n): return n  # identity sample

    for idx, chord in enumerate(prog.chords):
        OCTAVE = 4
        notes = [(OCTAVE + rand_octave_shift(spread)) * 12 + NOTE_TO_INT[c]
                 for c in chord.components()]
        # sampled_notes = np.random.choice(notes, rand_octave_shift(3))
        sampled_notes = sample_notes(notes)
        print(chord, chord.components(), notes, sampled_notes)
        left_offset = idx * duration
        right_offset = left_offset + duration - gap_size
        pianoroll[left_offset:right_offset, sampled_notes] = vel

    track = Track(pianoroll=pianoroll, program=0, is_drum=False,
                  name='my awesome piano')
    return track


def plot_track(track):
    fig, ax = track.plot()
    plt.show()


def write_to_mid(track, out_file, downbeat=[0, 96, 192, 288]):
    multitrack = Multitrack(
        tracks=[track], tempo=120.0, downbeat=downbeat, beat_resolution=24)
    multitrack.write(out_file)


def main(model_path=MODEL_OUT_PATH):
    mdl = load_mdl(model_path)
    # test_model(mdl)
    chrd = choose_random_chord(mdl)
    print("starting chord: ", chrd)
    # prog = generate_chord_progression(mdl, chrd, 20)
    prog = generate_hypercube_progression(chrd)
    track = generate_pianoroll_from_progression(prog, 20, 48)
    # plot_track(track)
    write_to_mid(track, 'test.mid', downbeat=[0, 48, 96, 144])


if __name__ == '__main__':
    main()
