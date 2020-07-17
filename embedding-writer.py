import numpy as np
import re
import os
import csv
import fasttext

from pychord import Chord
from hypercube import (
    bin_to_chord,
    bin_to_note_ints, note_ints_to_names, get_all_hypercube_vertices,
    get_neighbors_of_vert
)
from proll import INT_TO_NOTE
from generate import load_mdl

OUTPUT_PATH = 'outputs'


def write_csv_labels(fieldnames=[], row_dicts=[], f_name='labels.tsv'):
    with open(os.path.join(OUTPUT_PATH, f_name), 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            delimiter='\t',
            fieldnames=fieldnames
        )

        writer.writeheader()
        for row_dict in row_dicts:
            writer.writerow(row_dict)


def draw_hypercube():
    verts = get_all_hypercube_vertices()
    verts_arr = []
    verts_meta = []
    skip_nonchords = True  # sparse, but chords skipped.
    bytes_file_name = 'hypercube_verts_valid_chords.bytes'
    labels_file_name = 'hypercube_labels_valid_chords.tsv'
    fieldnames = ['chord_name', 'chord_notes', 'chord_binary']
    for vert in verts:
        vert_list = list(vert)
        vert_arr = np.array(vert_list)
        # verts_arr.append(vert_arr)
        try:
            chord_obj = bin_to_chord(vert_arr)
            if len(chord_obj):
                chord_name = str(chord_obj[0])
            else:
                chord_name = '-'
        except e:
            chord_name = '-'

        if skip_nonchords and chord_name != '-':
            verts_arr.append(vert_arr)
            chord_bin = ''.join([str(int(v)) for v in vert_list])
            chord_notes = note_ints_to_names(bin_to_note_ints(vert_arr))
            vert_meta = {
                'chord_name': chord_name,
                'chord_notes': '_'.join(list(chord_notes)),
                'chord_binary': chord_bin
            }
            verts_meta.append(vert_meta)

    verts_stack = np.vstack(verts_arr).astype(np.float32)
    print("tensor_shape: ", verts_stack.shape)
    verts_stack.tofile(os.path.join(OUTPUT_PATH, bytes_file_name))
    # print(vert_stack
    write_csv_labels(fieldnames=fieldnames,
                     row_dicts=verts_meta, f_name=labels_file_name)


def draw_embedding():
    MODEL_OUT_PATH = '../datasets/jazz_progressions.mdl.fasttext'
    verts_arr = []
    verts_meta = []
    bytes_file_name = 'jazz_embeddings.bytes'
    labels_file_name = 'jazz_labels.tsv'
    fieldnames = ['chord_name', 'chord_notes']
    mdl = load_mdl(MODEL_OUT_PATH)

    for word in mdl.words:
        emb = mdl[word]
        vert_arr = np.array(emb)
        chord_name = word
        if word != '</s>':
            verts_arr.append(vert_arr)
            chord_notes = Chord(word).components()
            vert_meta = {
                'chord_name': chord_name,
                'chord_notes': '_'.join(list(chord_notes)),
            }
            verts_meta.append(vert_meta)

    verts_stack = np.vstack(verts_arr).astype(np.float32)
    print("tensor_shape: ", verts_stack.shape)
    verts_stack.tofile(os.path.join(OUTPUT_PATH, bytes_file_name))
    # print(vert_stack
    write_csv_labels(fieldnames=fieldnames,
                     row_dicts=verts_meta, f_name=labels_file_name)

    return


def draw_graph():
    verts = get_all_hypercube_vertices()
    verts_arr = []
    verts_meta = []

    skip_nonchords = True  # sparse, but chords skipped.
    # fieldnames = ['chord_name', 'chord_notes', 'chord_binary']
    graph = {}
    for vert in verts:
        vert_list = list(vert)
        vert_arr = np.array(vert_list)
        try:
            chord_obj = bin_to_chord(vert_arr)
            if len(chord_obj):
                chord_name = str(chord_obj[0])
            else:
                chord_name = '-'
        except:
            chord_name = '-'

        neighbors = get_neighbors_of_vert(vert)
        if skip_nonchords and chord_name != '-':
            chord_bin = ''.join([str(int(v)) for v in vert_list])
            chord_notes = note_ints_to_names(bin_to_note_ints(vert_arr))
            vert_meta = {
                'chord_name': chord_name,
                'chord_notes': '_'.join(list(chord_notes)),
                'chord_binary': chord_bin
            }
            filtered_neighbors = []
            for n in neighbors:
                try:
                    chord_obj = bin_to_chord(np.array(list(n)))
                    if len(chord_obj):
                        filtered_neighbors.append(str(chord_obj[0]))
                except:
                    chord_obj = None
            graph[chord_name] = filtered_neighbors
            verts_meta.append(vert_meta)
    # graph as dictionary
    # print(graph)

    def sanitize(x):
        return x
        # return x.replace('/', '\/').replace('#',
        #                                     '\#').replace('+', '\+').replace('-', '\-')
    # graphviz format:
    with open("graph.viz", "w") as f:
        f.write('digraph G {\n')
        notes = [INT_TO_NOTE[i] for i in range(0, 12)]
        axis = '"notes" -> ' + '-> '.join([('"' + n + '"')
                                           for n in notes]) + ';'
        f.write('\t' + axis + '\n')
        # write ranks
        for note in notes:
            matching_notes = []
            if len(note) == 1:
                # non-sharp
                regex = re.compile(note + '[A-Za-z0-9]')
            else:
                # sharp
                regex = re.compile(note)
            for k in graph:
                if regex.match(k):
                    matching_notes.append(k)
            if matching_notes:
                ranks = '{ rank = same' + \
                    '; "' + note + '" ' + \
                    '; '.join([('"' + n + '"')
                               for n in matching_notes]) + '; }'
                f.write('\t' + ranks + '\n')
                # add links to note
                neighbors = ' '.join([('"' + n + '"')
                                      for n in matching_notes])
                l = '\t"' + note + '" -> ' + neighbors + '' + '\n'
                f.write('\t' + l + '\n')
        for k in graph:
            neighbors = ' '.join([('"' + n + '"') for n in graph[k]])
            s = '\t"' + sanitize(k) + '" -> ' + sanitize(neighbors) + '' + '\n'
            f.write(s)
        f.write('}\n')
        f.close()
    return


def main():
    # draw_hypercube()
    # draw_embedding()
    draw_graph()


if __name__ == '__main__':
    main()
