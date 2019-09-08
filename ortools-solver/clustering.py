import numpy as np
from sklearn.cluster import DBSCAN


# magic constants
min_radius = 12
max_radius = 42
min_no_clusters = 50
max_avg_cluster_size = 500
max_cluster_size = 500

def recursive_dbscan(X, indices, min_radius=min_radius, max_radius=max_radius):
    best_clusters = None
    best_cluster_size = 0
    while min_radius < max_radius:
        curr_radius = (min_radius + max_radius) / 2

        clusters = DBSCAN(eps=curr_radius, metric='cityblock').fit(X)
        no_clusters = len(np.unique(clusters))
        
        if no_clusters < min_no_clusters: # not enough clusters
            max_radius = curr_radius - 1
        else:
            min_radius = curr_radius + 1
            
        avg_cluster_size = np.histogram(clusters.labels_)[0].mean()

        if avg_cluster_size > best_cluster_size: # choose the biggest cluster possible
            best_cluster_size = avg_cluster_size
            best_clusters = clusters

    if best_clusters is None:
        return [indices]
    
    final_idx = [np.where(best_clusters.labels_ == i)[0] for i in np.unique(best_clusters.labels_)]
    final_indices = [indices[i] for i in final_idx]
    final_clusters = [X[i] for i in final_idx]
    new_clusters = []
    for cluster_indices, cluster in zip(final_indices, final_clusters):
        if len(cluster) > max_cluster_size:
            new_clusters.extend(recursive_dbscan(cluster, cluster_indices, 0.9999 * max_radius, 1.2 * max_radius))
        else:
            new_clusters.append(cluster_indices)
    return new_clusters