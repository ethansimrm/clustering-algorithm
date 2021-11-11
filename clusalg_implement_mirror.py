### Project 3: Closest Pairs and Clustering Algorithms
"""
Here we will implement five algorithms which compute
pairs and clusters.
"""

import math
import alg_cluster
import codeskulptor
codeskulptor.set_timeout(60)

def slow_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects cluster_list and returns a 
    closest pair where the pair is represented by the 
    tuple (dist, idx1, idx2), where dist is the distance 
    between cluster_list[idx1] and cluster_list[idx2]; idx1
    < idx2.
    
    This is a brute-force algorithm.
    """
    ans_tuple = (float("inf"), -1, -1)
    for point1 in cluster_list:
        for point2 in cluster_list:
            if point2 != point1:
                new_ans_tuple = (point1.distance(point2), 
                                 cluster_list.index(point1), 
                                 cluster_list.index(point2))
                if new_ans_tuple[0] < ans_tuple[0]:
                    ans_tuple = new_ans_tuple
    return ans_tuple

def fast_closest_pair(cluster_list):
    """
    Implements a divide-and-conquer approach to the same problem
    outlined above.
    
    Note that cluster_list is a sorted list - increasing order of 
    horizontal coordinates.
    """
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    if len(cluster_list) < 3:
        ans_tuple = slow_closest_pair(cluster_list)
    else:
        index_mid = len(cluster_list) / 2
        list_left = cluster_list[0 : index_mid]
        list_right = cluster_list[index_mid : len(cluster_list)]
        best_left = fast_closest_pair(list_left)
        pre_right = fast_closest_pair(list_right)
        best_right = (pre_right[0], pre_right[1] + index_mid, 
                      pre_right[2] + index_mid)
        if best_left[0] < best_right[0]:
            ans_tuple = best_left
        else:
            ans_tuple = best_right
        #We need to ask also if the closest distance lies between the 
        #last point in list_left and the first point in list_right
        mid_horiz = 0.5 * (list_left[-1].horiz_center() + list_right[0].horiz_center())
        mid_ans_tuple = closest_pair_strip(cluster_list, mid_horiz, ans_tuple[0])
        if mid_ans_tuple[0] < ans_tuple[0]:
            ans_tuple = mid_ans_tuple
    return ans_tuple
    
def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Takes a list of Cluster objects and two floats horiz_center 
    and half_width. horiz_center specifies the horizontal position 
    of the center line for a vertical strip. half_width specifies the 
    maximal distance of any point in the strip from the center line. 
    
    Returns a tuple corresponding to the closest pair of clusters which 
    lie within the specified strip.
    """
    list_s = []
    for point in cluster_list:
        if math.fabs(point.horiz_center() - horiz_center) < half_width:
            list_s.append(point)
    list_s.sort(key = lambda cluster: cluster.vert_center())
    ans_tuple = (float("inf"), -1, -1)
    for idx_1 in range(0, len(list_s) - 1):
        for idx_2 in range(idx_1 + 1, min(idx_1 + 3, len(list_s) - 1) + 1):
            new_ans_tuple = (list_s[idx_1].distance(list_s[idx_2]), 
                             cluster_list.index(list_s[idx_1]),
                             cluster_list.index(list_s[idx_2]))
            if cluster_list.index(list_s[idx_1]) > cluster_list.index(list_s[idx_2]):
                new_ans_tuple = (new_ans_tuple[0], new_ans_tuple[2], new_ans_tuple[1])
            if new_ans_tuple[0] < ans_tuple[0]:
                ans_tuple = new_ans_tuple
    return ans_tuple

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Takes a list of Cluster objects, cluster_list, and applies 
    hierarchical clustering to this list of clusters. This 
    clustering process should proceed until num_clusters clusters remain. 
    
    The function then returns this list of clusters.
    """
    current_clusters = []
    for cluster in cluster_list:
        current_clusters.append(cluster.copy())
    while len(current_clusters) > num_clusters:
        (dummy_dist, idx_1, idx_2) = fast_closest_pair(current_clusters)
        current_clusters[idx_1].merge_clusters(current_clusters[idx_2])
        current_clusters.pop(idx_2)
    return current_clusters

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Takes a list of Cluster objects cluster_list and applies k-means 
    clustering to this list of clusters. 
    
    This function should compute an initial list of clusters (line 2 
    in the pseudo-code) with the property that each cluster consists 
    of a single county chosen from the set of the num_cluster counties 
    with the largest populations. 
    
    The function should then compute num_iterations of k-means clustering 
    and return this resulting list of clusters.
    """
    new_list = []
    for cluster in cluster_list:
        new_list.append(cluster.copy())
    new_list.sort(key = lambda cluster: cluster.total_population())
    new_list.reverse()
    centers_list = []
    for idx in range(0, num_clusters):
        centers_list.append(new_list[idx])
    for dummy_iterations in range(0, num_iterations):
        ans_cluster_list = []
        for dummy_clusters in range (num_clusters):
            ans_cluster_list.append(alg_cluster.Cluster(set([]), 0, 0, 0, 0))
        for cluster_idx in range(len(new_list)):
            min_dist = float("inf")
            min_center = -1
            for center_idx in range(0, num_clusters):
                dist = new_list[cluster_idx].distance(centers_list[center_idx])
                if dist < min_dist:
                    min_dist = dist
                    min_center = center_idx
            ans_cluster_list[min_center].merge_clusters(new_list[cluster_idx])
        for center_idx in range(0, num_clusters):
            centers_list[center_idx] = ans_cluster_list[center_idx]
    return centers_list
 
# Lessons learnt from k-means clustering - copy the list so you don't mutate input, and don't use the 
# * operator to add stuff to a list when it's a user-created class!
    
    
