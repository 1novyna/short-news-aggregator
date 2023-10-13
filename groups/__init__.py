from .embed import add_embedding
from .cluster import add_clusters
from .title import add_titles


def group_with_titles(data, groups_number):
    import numpy as np
    import pandas as pd

    df = pd.DataFrame(data, columns=["Text"])
    df = add_embedding(df)

    matrix = np.vstack(df.Embedding.values)
    df = add_clusters(df, matrix, n_clusters=groups_number)

    df = add_titles(df, n_clusters=groups_number)
    return df.values.tolist()
