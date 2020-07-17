from pychord import Chord, note_to_chord
import numpy as np
import itertools
from scipy.spatial import distance
from tonegraph.graph import bin_to_chord, bin_to_note_ints, chord_to_binary, notes_to_bin

from proll import INT_TO_NOTE, NOTE_TO_INT

BIN_ARR = np.zeros(12, dtype=int)
NOTE_INTS_ARR = np.array(range(0, 12))


def get_all_hypercube_vertices():
    mins = np.zeros(12)
    maxs = np.full(12, 1)
    verts = list(itertools.product(*zip(mins, maxs)))
    print("num_verts: ", len(verts))
    return verts


def get_neighbors_of_vert(vert):
    """
    binary tuple = vert
    """

    neighbors = []
    for i, d in enumerate(vert):
        # flip bit
        n = int(not d)
        vert_list = list(vert)
        vert_list[i] = n
        neighbors.append(tuple(vert_list))
    return neighbors


def get_random_path(start_vert, length):
    path = [start_vert]
    for i in range(0, length):
        neighbors = get_neighbors_of_vert(path[-1])
        # print("neighbors: ", neighbors)
        # np.random.shuffle(neighbors)
        n = None
        # print("neighbors shuffled: ", neighbors)
        while not n or n in path:
            # rand_idx = int(np.random.rand() * len(neighbors))
            n = neighbors.pop()
            # keep refilling neighbors
            if not neighbors:
                neighbors = get_neighbor_of_vert(n)
        path.append(n)
    return path


def get_random_outward_path(start_vec, length):
    path = [start_vec]
    for i in range(0, length):
        neighbors = get_neighbors_of_vert(path[-1])
        hammings = [hamming_distance(start_vec, n) for n in neighbors]
        # increase hamming distance from start each step
        outward_neighbors = [
            n for j, n in enumerate(neighbors) if (hammings[j] >= 1)]
        # print("neighbors: ", i, neighbors)
        # print("hammings: ", hammings)
        # print("outward: ", outward_neighbors)
        np.random.shuffle(outward_neighbors)
        # dead end for some reason?
        if not outward_neighbors:
            return path
        else:
            path.append(outward_neighbors[0])
    return path


def hamming_distance(v1, v2):
    """
    takes the hamming distance of 2 binary tuples
    """
    return distance.hamming(v1, v2)


def get_hypercube_neighbor_path(start_note_ints, max_walk=100, outward_path=True):
    bin_notes = notes_to_bin(start_note_ints)
    vert = tuple(bin_notes)
    if outward_path:
        path = get_random_outward_path(vert, max_walk)
    else:
        path = get_random_path(vert, max_walk)
    path_chords = [bin_to_chord(np.array(n)) for n in path]
    non_empty_chords = [c_arr[0] for c_arr in path_chords if len(c_arr)]
    return non_empty_chords


def main():
    test = [0, 4, 7]
    # all_chords = itertools.combinations((0, 1), 12)
    # print("num_all_chords: ", len(list(all_chords)))
    # test = NOTE_INTS_ARR.tolist()
    # test = [0, 1, 2, 3, 4, 5, 6, 7]
    print("test: ", test)
    notes = note_ints_to_names(test)
    print("notes: ", notes)
    bin_notes = notes_to_bin(test)
    print("bin_notes: ", bin_notes)
    chrd = bin_to_chord(bin_notes)
    if not chrd:
        print("no chord.")
    else:
        print("chrd", chrd, str(chrd[0]))
        print("reverse: ", chord_to_binary(str(chrd[0])))
    verts = get_all_hypercube_vertices()
    rand_idx = int(np.random.rand() * len(verts))
    vert = verts[rand_idx]
    # print("vert: ", vert)
    # print("neighbors: ", get_neighbors_of_vert(vert))

    print("random_path: ", get_hypercube_neighbor_path(test))
    print("random_outward_path: ",
          get_hypercube_neighbor_path(test, outward_path=True))

    # test_vert = tuple(bin_notes)
    # test_neighbors = get_neighbors_of_vert(test_vert)
    # print(test_neighbors)
    # chords = [bin_to_chord(np.array(n)) for n in test_neighbors]
    # print(chords)

    # # path = get_random_path(test_vert, 12)
    # path = get_random_path(test_vert, 100)
    # path_chords = [bin_to_chord(np.array(n)) for n in path]
    # print(path_chords)

    return


if __name__ == '__main__':
    main()
