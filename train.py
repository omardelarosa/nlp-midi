import fasttext


# CORPUS_PATH = '../datasets/jazz_progressions.txt'
# MODEL_OUT_PATH = '../datasets/jazz_progressions.mdl.fasttext'

CORPUS_PATH = '../datasets/maestro_progressions.txt'
MODEL_OUT_PATH = '../datasets/maestro_progressions.mdl.fasttext'

model = fasttext.train_unsupervised(
    CORPUS_PATH,
    model='skipgram',
    minn=0,
    maxn=4,
    verbose=4
)

model.save_model(MODEL_OUT_PATH)

# print(model.words)

# quick test
for word in model.words[0:10]:
    neighbors = model.get_nearest_neighbors(word)
    neighbor_chords = [n[1] for n in neighbors]
    print("chord: {}, neighbors: {}".format(word, neighbor_chords[0:10]))
