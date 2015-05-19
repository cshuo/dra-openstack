__author__ = 'pike'

#enum ResourceType
class ResourceType:
    (CPU_UTIL, BANDWIDTH, DISK_IO) = ('CPU_UTIL', 'BANDWIDTH', 'DISK_IO')

#enum ResourceType
class InstanceType:
    (ALL, MATLAB_1, MATLAB_1_MASTER, MATLAB_2, MATLAB_2_MASTER, WEB_SERVER_1, GAME_1, STORAGE_1, HADOOP) = ('ALL', 'MATLAB', 'MATLAB_MASTER', 'MATLAB_2', 'MATLAB_2_MASTER', 'WEB_SERVER_1', 'GAME', 'STORAGE_1', 'HADOOP')


#distance between hosts
host_distance_matrix = [[0.5, 2, 3, 4],
                        [2, 0.5, 2, 3],
                        [3, 2, 0.5, 2],
                        [4, 3, 2, 0.5]]

host_mapper = {'host_1' : 0, 'host_2' : 1, 'host_3' : 2, 'host_4' : 3}