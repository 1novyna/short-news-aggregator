from sklearn.cluster import KMeans


def add_clusters(df, matrix, n_clusters=4):
    kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42)
    kmeans.fit(matrix)
    labels = kmeans.labels_
    df["Cluster"] = labels

    df.groupby("Cluster")

    return df
