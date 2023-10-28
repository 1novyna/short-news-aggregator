import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster._hdbscan.hdbscan import HDBSCAN


def queryset_to_data_frame(queryset):
    values = list(queryset.values())
    return pd.DataFrame(values)


def clusterize(df):
    scaler = StandardScaler()
    matrix = np.vstack(df.embedding.values)
    scaled_matrix = scaler.fit_transform(matrix)

    hdbscan = HDBSCAN(
        min_cluster_size=3,
        algorithm="kdtree",
        cluster_selection_method="leaf",
    )
    hdbscan.fit(scaled_matrix)

    df["cluster"] = hdbscan.labels_

    return df
