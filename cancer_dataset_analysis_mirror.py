"""
Algorithmic Thinking 2 Application 3

Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = False

import math
import random
import urllib2
import alg_cluster
import time

# conditional imports
if DESKTOP:
    import alg_project3_solution      # desktop project solution
    import alg_clusters_matplotlib
else:
    import user48_f7BRIhoAqU_52 as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(5000)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
#    cluster_list = sequential_clustering(singleton_list, 15)	
#    print "Displaying", len(cluster_list), "sequential clusters"

#    cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
#    print "Displaying", len(cluster_list), "hierarchical clusters"

    cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)	
    print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers
    
#run_example()

##Algorithmic Thinking Application 3 Question 1

def gen_random_clusters(num_clusters):
    """
    This function generates a list of clusters where
    each cluster corresponds to one randomly generated
    point in a square with corners (+- 1, +- 1).
    """
    cluster_list = []
    for dummy_idx in range(num_clusters):
        horiz_pos = random.random() * 2 - 1
        vert_pos = random.random() * 2 - 1
        new_cluster = alg_cluster.Cluster(set([]),horiz_pos, 
                                          vert_pos, 0, 0)
        cluster_list.append(new_cluster)
    return cluster_list
        
def timer(function, input_data):
    """
    Returns time taken for a function to evaluate input_data
    of the user's choice.
    """
    start_time = time.time()
    function(input_data)
    end_time = time.time()
    duration = end_time - start_time
    return duration

def time_check(function):
    """
    Returns a list of tuples of form (num_clusters, time)
    for functions of the user's choice tested on lists from
    gen_random_clusters(num_clusters) where num_clusters varies
    from 2 to 200.
    """
    output = []
    for num_clusters in range(2, 201):
        cluster_list = gen_random_clusters(num_clusters)
        time_taken = timer(function, cluster_list)
        output.append((num_clusters, time_taken))
    return output

#slow_time = time_check(alg_project3_solution.slow_closest_pair)
#fast_time = time_check(alg_project3_solution.fast_closest_pair)
#        
#simpleplot.plot_lines("CodeSkulptor Running Times of slow_closest_pair and fast_closest_pair", 
#                      600, 600, 
#                      "N(Initial Clusters)", 
#                      "Running Time (Seconds)", 
#                      [slow_time, fast_time], False, 
#                      ["slow_closest_pair", "fast_closest_pair"]) 

##Questions 2 and 3:

#Modify accordingly: data_table = load_data_table(DATA_3108_URL)

##Question 4:

#In the worst-case, hierarchical clustering should have
#O(n) initialisations and n calls to O(nlog^2(n))
#fast_closest_pair AND the union and difference operations both
#of worst-case O(n). This means it is O((n-k)*(n + nlog^2(n))).

#In comparison, k-means clustering seems to be of O(qkn).

##Questions 5 and 6:

#Modify accordingly: data_table = load_data_table(DATA_111_URL)

##Question 7

def compute_distortion(cluster_list, data_table):
    """
    Computes total distortion for a cluster list using the data source.
    
    Returns a float.
    """
    cumulative_distortion = 0.0
    for cluster in cluster_list:
        cumulative_distortion += cluster.cluster_error(data_table)
    return cumulative_distortion

#data_table = load_data_table(DATA_290_URL)
#    
#singleton_list = []
#for line in data_table:
#    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
#
#list_a = alg_project3_solution.hierarchical_clustering(singleton_list, 16)
#list_b = alg_project3_solution.kmeans_clustering(singleton_list,16, 5)

#print compute_distortion(list_a, data_table)
  
## Question 10

def hierarchical_tester(data_url):
    """
    Takes an input and returns a list of tuples of the form 
    (n(output clusters), cumulative distortion) for hierarchical clustering.
    """
    data_table = load_data_table(data_url)    
    cluster_list = []
    for line in data_table:
        cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    output_list = []
    for output_cluster_num in range(20, 5, -1):
        cluster_list = alg_project3_solution.hierarchical_clustering(cluster_list, output_cluster_num)
        error = compute_distortion(cluster_list, data_table)
        output_list.append((output_cluster_num, error))
    output_list.reverse()
    return output_list

def k_means_tester(data_url):
    """
    Takes an input and returns a list of tuples of the form 
    (n(output clusters), cumulative distortion) for k-means clustering.
    """
    data_table = load_data_table(data_url)    
    cluster_list = []
    for line in data_table:
        cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    output_list = []
    for output_cluster_num in range(6, 21):
        test_list = alg_project3_solution.kmeans_clustering(cluster_list, output_cluster_num, 5)
        error = compute_distortion(test_list, data_table)
        output_list.append((output_cluster_num, error))
    return output_list

#h_test_111 = hierarchical_tester(DATA_111_URL)
#h_test_290 = hierarchical_tester(DATA_290_URL)
#h_test_896 = hierarchical_tester(DATA_896_URL) 
        
#k_test_111 = k_means_tester(DATA_111_URL)
#k_test_290 = k_means_tester(DATA_290_URL)
#k_test_896 = k_means_tester(DATA_896_URL)

import simpleplot

#simpleplot.plot_lines("Distortion resulting from hierarchical and k-means clustering performed on an 111-county dataset", 
#                      600, 600, 
#                      "N(Output Clusters)", 
#                      "Distortion", 
#                      [h_test_111, k_test_111], False, 
#                      ["Hierarchical Clustering", "k-means Clustering"]) 

#simpleplot.plot_lines("Distortion resulting from hierarchical and k-means clustering performed on a 290-county dataset", 
#                      600, 600, 
#                      "N(Output Clusters)", 
#                      "Distortion", 
#                      [h_test_290, k_test_290], False, 
#                      ["Hierarchical Clustering", "k-means Clustering"])         

#simpleplot.plot_lines("Distortion resulting from hierarchical and k-means clustering performed on an 896-county dataset", 
#                      600, 600, 
#                      "N(Output Clusters)", 
#                      "Distortion", 
#                      [h_test_896, k_test_896], False, 
#                      ["Hierarchical Clustering", "k-means Clustering"]) 


