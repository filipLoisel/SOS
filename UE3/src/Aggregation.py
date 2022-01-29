import numpy as np
from numpy.random import randint
from scipy.cluster.hierarchy import ward, fcluster


def distance(l1, l2):
    "l1 and l2 need to be 2 dimensional numpy arrays"
    distance_normal = 0
    distance_reversed = 0
    for i in range(len(l1)):
        distance_normal += np.linalg.norm(l1[i] - l2[i])
        distance_reversed += np.linalg.norm(l1[i] - l2[-(i + 1)])
    l = [distance_normal, distance_reversed]
    return min(l), np.where(l == min(l))[0][0]  # [0][0] to get an int instead of an array


def create_distance_matrix(lines):
    # create mattrix that shows if the pairwise distance is revesed or not
    n_lines = lines.shape[0]
    matrix = np.empty((n_lines, n_lines))
    normal_or_not = np.empty((n_lines, n_lines))
    for i in range(n_lines):
        for j in range(n_lines):
            if i == j:
                matrix[i, j] = np.inf
                normal_or_not[i, j] = -1
            else:
                matrix[i, j] = distance(lines[i], lines[j])[0]
                normal_or_not[i, j] = distance(lines[i], lines[j])[1]

    return np.triu(matrix, 1), normal_or_not


def assign_clusters(d_matrix, threshold, print_Z=False):
    Z = ward(d_matrix[d_matrix > 0])
    # see link for explanation of Z
    # https://docs.scipy.org/doc/scipy/reference/reference/generated/scipy.cluster.hierarchy.fcluster.html#scipy.cluster.hierarchy.fcluster
    if print_Z:
        print(Z)
    assigned_clusters = fcluster(Z, threshold, criterion='distance')
    return assigned_clusters


def average_lines(lines, clusters, r_matrix, names):
    ''' averages x,y values of all lines per cluster
    '''

    reverse_list = []
    final_lines = []
    final_names = []
    for i in range(max(clusters)):  # iterate trough clusters
        reverse_used = False #indicates if the cluster contains a reversed line
        cluster_lines = np.where(clusters == i + 1)
        if len(cluster_lines[0]) == 1:
            final_lines.append(lines[cluster_lines[0]][0].tolist())
            final_names.append(names[cluster_lines[0][0]])
            reverse_list.append(reverse_used)
            continue

        first_ind = cluster_lines[0][0]
        name = names[first_ind]
        averaged_line = lines[first_ind]
        for compare_ind in cluster_lines[0]:  # itearate trough lines
            if r_matrix[first_ind, compare_ind] == 0:  # normal distance
                averaged_line = averaged_line + lines[compare_ind]
                name += " + " + names[compare_ind]

            elif r_matrix[first_ind, compare_ind] == 1:  # reverse distance
                name += " + " + names[compare_ind]
                reverse_used = True
                averaged_line = averaged_line + np.flip(lines[compare_ind], axis=0)
        averaged_line = (averaged_line / len(cluster_lines[0])).tolist()
        reverse_list.append(reverse_used)
        final_lines.append(averaged_line)
        final_names.append(name)

    return final_lines, final_names, reverse_list


def aggregate(lines, threshold, names, print_Z=False):
    d_matrix, r_matrix = create_distance_matrix(lines)
    clusters = assign_clusters(d_matrix, threshold, print_Z)
    new_lines = average_lines(lines, clusters, r_matrix, names)
    new_lines = np.array(new_lines)
    return new_lines




if __name__ == '__main__':
    names = ['a','b','c']
    #lines = create_lines()
    lines = [[[ 3.66101695,  6.23728814],
  [ 6.18181818,  9.03030303],
  [ 9.25806452,  9.64516129],
  [12.63636364,  3.57575758],
  [19.09623431, 10.56903766],
  [21.19211823, 11.09852217],
  [25.73809524,  6.95238095],
  [28.3877551,   5.67346939],
  [28.73913043,  6.36956522],
  [27.93846154, 13.46153846]],

 [[11.16216216, 16.47297297],
  [16.85454545, 13.27272727],
  [20.17857143, 10.89285714],
  [17.75630252,  7.97478992],
  [19.83783784,  8.36936937],
  [19.34042553, 11.55319149],
  [20.70175439, 10.56140351],
  [20.08510638,  8.14893617],
  [22.48,        5.7       ],
  [26.95,        2.5625    ]],

 [[34.97014925, 12.79104478],
  [31.05882353, 11.        ],
  [28.9375,      9.21875   ],
  [26.23333333, 16.06666667],
  [20.86915888,  8.30373832],
  [17.20253165,  8.06329114],
  [10.82051282, 12.38461538],
  [10.97560976, 12.2195122 ],
  [ 9.61363636, 12.25],
  [10.48387097,  6.14516129]]]
    lines = np.array(lines)
    new_lines,names, reverse_list = aggregate(lines, 80 ,names)
    print(names,reverse_list)
   # print("Original lines {} \nAggregated lines {}".format(lines,new_lines))
    #print(new_lines)
    #print(np.array(new_lines).shape)











