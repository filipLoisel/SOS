import numpy as np
from numpy.random import randint
from scipy.cluster.hierarchy import ward, fcluster


def create_lines(n_rows = 5, n_columns = 6):
    lines = []
    for i in range(n_rows):
        lines.append([(randint(0,10),randint(0,10)) for _ in range(n_columns)])
    return np.array(lines)


def distance(l1,l2):
    "l1 and l2 need to be 2 dimensional numpy arrays"
    distance_normal = 0
    distance_reversed = 0
    for i in range(len(l1)):
        distance_normal += np.linalg.norm(l1[i] - l2[i])
        distance_reversed += np.linalg.norm(l1[i] - l2[-(i+1)])
    l = [distance_normal, distance_reversed]
    return min(l),np.where(l == min(l))[0][0] # [0][0] to get an int instead of an array


def create_distance_matrix(lines):
    # create mattrix that shows if the pairwise distance is revesed or not
    n_lines = lines.shape[0]
    matrix = np.empty((n_lines,n_lines))
    normal_or_not = np.empty((n_lines,n_lines))
    for i in range(n_lines):
        for j in range(n_lines):
            if i == j:
                matrix[i,j] = np.inf
                normal_or_not[i,j] = -1
            else:
                matrix[i,j] = distance(lines[i],lines[j])[0]
                normal_or_not[i,j] = distance(lines[i],lines[j])[1]

    return np.triu(matrix,1), normal_or_not


def assign_clusters(d_matrix,threshold,print_Z=False):
    Z = ward(d_matrix[d_matrix > 0])
    # see link for explanation of Z
    # https://docs.scipy.org/doc/scipy/reference/reference/generated/scipy.cluster.hierarchy.fcluster.html#scipy.cluster.hierarchy.fcluster
    if print_Z:
        print(Z)
    assigned_clusters = fcluster(Z, threshold, criterion='distance')
    return assigned_clusters

def average_lines(lines,clusters,r_matrix):
    ''' averages x,y values of all lines per cluster
    '''
    final_lines = []
    for i in range(max(clusters)-1): #iterate trough clusters
        cluster_lines = np.where(clusters == i + 1)
        if len(cluster_lines) == 1:
            final_lines.append(lines[cluster_lines[0]])


        first_ind = cluster_lines[0][0]
        averaged_line = lines[first_ind]
        for compare_ind in cluster_lines[0]:   #itearate trough lines
            if r_matrix[first_ind, compare_ind] == 0:  # normal distance
                averaged_line = averaged_line + lines[compare_ind]

            elif r_matrix[first_ind, compare_ind] == 1:  # reverse distance
                averaged_line = averaged_line + np.flip(lines[compare_ind])
        averaged_line / len(cluster_lines)
        final_lines.append(averaged_line)
    return final_lines


def aggregate(lines,threshold):
    d_matrix, r_matrix = create_distance_matrix(lines)
    clusters = assign_clusters(d_matrix, threshold)
    new_lines = average_lines(lines, clusters, r_matrix)
    return new_lines




if __name__ == '__main__':
    lines = create_lines()
    new_lines = aggregate(lines, 28)
    print("Original lines {} \nAggregated lines {}".format(lines,new_lines))










