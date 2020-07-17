import fasttext

# DEFAULT TEST VALUES

# CORPUS_PATH = '../datasets/jazz_progressions.txt'
# MODEL_OUT_PATH = './models/jazz_progressions-12d.mdl.fasttext'

CORPUS_PATH = '../datasets/maestro_progressions.txt'
MODEL_OUT_PATH = './models/maestro_progressions-12d.mdl.fasttext'


def train(corpus_path, model_out_path):
    model = fasttext.train_unsupervised(
        corpus_path,
        model='skipgram',
        minn=0,
        maxn=4,
        dim=12,
        t=1.0,
        verbose=4
    )

    model.save_model(model_out_path)

    # quick test
    for word in model.words[0:10]:
        neighbors = model.get_nearest_neighbors(word)
        neighbor_chords = [n[1] for n in neighbors]
        print("chord: {}, neighbors: {}".format(word, neighbor_chords[0:10]))


if __name__ == '__main__':
    train(
        corpus_path=CORPUS_PATH,
        model_out_path=MODEL_OUT_PATH
    )
