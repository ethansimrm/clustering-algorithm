# clustering-algorithm

This is my solution to a clustering problem formulated as part of the Algorithmic Thinking course, which was organised by Rice University's Department of Computer Science.

Here, I implement the Slow_Closest_Pair, Fast_Closest_Pair and Closest_Pair_Strip algorithms to calculate the closest pair of clusters/points in a list. I then implement the Hierarchial_Clustering and Kmeans_Clustering algorithms to arrive at a specified number of clusters from a given list of points.

My work thus far is mirrored in clusalg_implement_mirror.py, and due to the highly specific nature of the modules imported, can only run in CodeSkulptor (a browser-based IDE also created by the Rice University Department of Computer Science) - you can access it at https://py2.codeskulptor.org/#user48_f7BRIhoAqU_53.py.

I then apply these algorithms to a dataset of lifetime cancer risk from air toxics across 3108 USA counties, with varying thresholds of lifetime cancer risk (multiplied by 10^-5). Taking only counties above the thresholds 3.5, 4.5, and 5.5 yields smaller data sets with 896, 290, and 111 counties, respectively - these are smaller datasets also employed in my code. The value of this exercise is not so much the conclusions gleaned about cancer risk but the relative performance of the algorithms on the same dataset. Notably, k-means clustering is much faster than this implementation of hierarchical clustering, but k-means clustering may suffer from higher distortion on smaller datasets if the choice of initial centres is not judicious. That said, both methods do not substantially differ in distortion on larger datasets.

This second portion is mirrored in cancer_dataset_analysis.py, and again, due to the highly specific nature of the modules imported, can only run in CodeSkulptor. It can be accessed at https://py2.codeskulptor.org/#user48_8GUbfAD0ww_30.py.
