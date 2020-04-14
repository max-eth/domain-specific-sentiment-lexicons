from socialsent.representations.embedding import SVDEmbedding, Embedding
from socialsent.representations.explicit import Explicit


def create_representation(rep_type, path, *args, **kwargs):
    if rep_type == "Explicit":
        return Explicit.load(path, *args, **kwargs)
    elif rep_type == "SVD":
        return SVDEmbedding(path, *args, **kwargs)
    else:
        return Embedding.load(path, *args, **kwargs)
