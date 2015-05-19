__author__ = 'pike'

# in our simulation, the workload refers to the load of each hour in a day, and is periodical
# each host has 24 vcpu and allocate 2 vcpu to each instance
# each host has 1G bandwidth each instance usually use 100M

import matplotlib.pyplot as plt

import tornado.web
import tornado.ioloop
import tornado.websocket

import time

from Utils.SshUtil import Ssh_tool
from Entity import *
from RuleWorker import *
from Util import *

exp = 4

#global host and instance list
host_list = {}
instance_list = {}

#global time count
time_count = 0



############################################### experiment setup ###############################################

def setup_environment_1():
    host_1 = Host('host_1', host_list)
    host_2 = Host('host_2', host_list)
    host_3 = Host('host_3', host_list)
    host_4 = Host('host_4', host_list)

    instance_master_1 = Instance_Matlab_1('instance_master_1', InstanceType.MATLAB_1_MASTER, host_1, instance_list)
    instance_master_2 = Instance_Matlab_2('instance_master_2', InstanceType.MATLAB_2_MASTER, host_2, instance_list)

    instance_1 = Instance_Matlab_1('instance_1', InstanceType.MATLAB_1, host_1, instance_list)
    instance_2 = Instance_Matlab_1('instance_2', InstanceType.MATLAB_1, host_1, instance_list)
    instance_3 = Instance_Matlab_1('instance_3', InstanceType.MATLAB_1, host_4, instance_list)
    instance_4 = Instance_Matlab_1('instance_4', InstanceType.MATLAB_1, host_2, instance_list)
    instance_5 = Instance_Matlab_1('instance_5', InstanceType.MATLAB_1, host_2, instance_list)
    instance_6 = Instance_Matlab_1('instance_6', InstanceType.MATLAB_1, host_4, instance_list)
    instance_7 = Instance_Matlab_1('instance_7', InstanceType.MATLAB_1, host_3, instance_list)
    instance_8 = Instance_Matlab_1('instance_8', InstanceType.MATLAB_1, host_3, instance_list)
    instance_9 = Instance_Matlab_1('instance_9', InstanceType.MATLAB_1, host_3, instance_list)
    instance_10 = Instance_Matlab_1('instance_10', InstanceType.MATLAB_1, host_4, instance_list)
    instance_11 = Instance_Matlab_1('instance_11', InstanceType.MATLAB_1, host_4, instance_list)
    instance_12 = Instance_Matlab_1('instance_12', InstanceType.MATLAB_1, host_4, instance_list)

    instance_13 = Instance_Matlab_2('instance_13', InstanceType.MATLAB_2, host_1, instance_list)
    instance_14 = Instance_Matlab_2('instance_14', InstanceType.MATLAB_2, host_1, instance_list)
    instance_15 = Instance_Matlab_2('instance_15', InstanceType.MATLAB_2, host_4, instance_list)
    instance_16 = Instance_Matlab_2('instance_16', InstanceType.MATLAB_2, host_2, instance_list)
    instance_17 = Instance_Matlab_2('instance_17', InstanceType.MATLAB_2, host_2, instance_list)
    instance_18 = Instance_Matlab_2('instance_18', InstanceType.MATLAB_2, host_4, instance_list)
    instance_19 = Instance_Matlab_2('instance_19', InstanceType.MATLAB_2, host_3, instance_list)
    instance_20 = Instance_Matlab_2('instance_20', InstanceType.MATLAB_2, host_3, instance_list)
    instance_21 = Instance_Matlab_2('instance_21', InstanceType.MATLAB_2, host_3, instance_list)
    instance_22 = Instance_Matlab_2('instance_22', InstanceType.MATLAB_2, host_4, instance_list)
    instance_23 = Instance_Matlab_2('instance_23', InstanceType.MATLAB_2, host_4, instance_list)
    instance_24 = Instance_Matlab_2('instance_24', InstanceType.MATLAB_2, host_4, instance_list)

def setup_environment_2():
    host_1 = Host('host_1', host_list)
    host_2 = Host('host_2', host_list)
    host_3 = Host('host_3', host_list)
    host_4 = Host('host_4', host_list)

    instance_1 = Instance_Game_1('instance_1', InstanceType.GAME_1, host_1, instance_list)
    instance_2 = Instance_Game_1('instance_2', InstanceType.GAME_1, host_1, instance_list)
    instance_3 = Instance_Game_1('instance_3', InstanceType.GAME_1, host_1, instance_list)
    instance_4 = Instance_Game_1('instance_4', InstanceType.GAME_1, host_1, instance_list)
    instance_5 = Instance_Game_1('instance_5', InstanceType.GAME_1, host_1, instance_list)
    instance_6 = Instance_Game_1('instance_6', InstanceType.GAME_1, host_1, instance_list)
    instance_7 = Instance_Game_1('instance_7', InstanceType.GAME_1, host_1, instance_list)
    instance_8 = Instance_Game_1('instance_8', InstanceType.GAME_1, host_2, instance_list)
    instance_9 = Instance_Game_1('instance_9', InstanceType.GAME_1, host_2, instance_list)
    instance_10 = Instance_Game_1('instance_10', InstanceType.GAME_1, host_2, instance_list)
    instance_11 = Instance_Game_1('instance_11', InstanceType.GAME_1, host_2, instance_list)
    instance_12 = Instance_Game_1('instance_12', InstanceType.GAME_1, host_2, instance_list)
    instance_13 = Instance_Game_1('instance_13', InstanceType.GAME_1, host_2, instance_list)
    instance_14 = Instance_Game_1('instance_14', InstanceType.GAME_1, host_2, instance_list)
    instance_15 = Instance_Game_1('instance_15', InstanceType.GAME_1, host_2, instance_list)

    instance_16 = Instance_Storage_1('instance_16', InstanceType.STORAGE_1, host_1, instance_list)
    instance_17 = Instance_Storage_1('instance_17', InstanceType.STORAGE_1, host_1, instance_list)
    instance_18 = Instance_Storage_1('instance_18', InstanceType.STORAGE_1, host_1, instance_list)
    instance_19 = Instance_Storage_1('instance_19', InstanceType.STORAGE_1, host_1, instance_list)
    instance_20 = Instance_Storage_1('instance_20', InstanceType.STORAGE_1, host_1, instance_list)
    instance_21 = Instance_Storage_1('instance_21', InstanceType.STORAGE_1, host_1, instance_list)
    instance_22 = Instance_Storage_1('instance_22', InstanceType.STORAGE_1, host_1, instance_list)
    instance_23 = Instance_Storage_1('instance_23', InstanceType.STORAGE_1, host_2, instance_list)
    instance_24 = Instance_Storage_1('instance_24', InstanceType.STORAGE_1, host_2, instance_list)
    instance_25 = Instance_Storage_1('instance_25', InstanceType.STORAGE_1, host_2, instance_list)
    instance_26 = Instance_Storage_1('instance_26', InstanceType.STORAGE_1, host_2, instance_list)
    instance_27 = Instance_Storage_1('instance_27', InstanceType.STORAGE_1, host_2, instance_list)
    instance_28 = Instance_Storage_1('instance_28', InstanceType.STORAGE_1, host_2, instance_list)
    instance_29 = Instance_Storage_1('instance_29', InstanceType.STORAGE_1, host_2, instance_list)
    instance_30 = Instance_Storage_1('instance_30', InstanceType.STORAGE_1, host_2, instance_list)

def setup_environment_3():
    host_1 = Host_Hadoop('host_1', host_list)
    host_2 = Host_Hadoop('host_2', host_list)
    host_3 = Host_Hadoop('host_3', host_list)
    host_4 = Host_Hadoop('host_4', host_list)

    host_1.addFile('file1')
    host_1.addFile('file5')
    host_2.addFile('file2')
    host_2.addFile('file6')
    host_3.addFile('file3')
    host_3.addFile('file7')
    host_4.addFile('file4')
    host_4.addFile('file8')

    instance_1 = Instance_Hadoop('instance_1', InstanceType.HADOOP, host_1, instance_list)
    instance_2 = Instance_Hadoop('instance_2', InstanceType.HADOOP, host_1, instance_list)
    instance_3 = Instance_Hadoop('instance_3', InstanceType.HADOOP, host_2, instance_list)
    instance_4 = Instance_Hadoop('instance_4', InstanceType.HADOOP, host_2, instance_list)
    instance_5 = Instance_Hadoop('instance_5', InstanceType.HADOOP, host_2, instance_list)
    instance_6 = Instance_Hadoop('instance_6', InstanceType.HADOOP, host_3, instance_list)
    instance_7 = Instance_Hadoop('instance_7', InstanceType.HADOOP, host_3, instance_list)
    instance_8 = Instance_Hadoop('instance_8', InstanceType.HADOOP, host_3, instance_list)
    instance_9 = Instance_Hadoop('instance_9', InstanceType.HADOOP, host_3, instance_list)
    instance_10 = Instance_Hadoop('instance_10', InstanceType.HADOOP, host_4, instance_list)
    instance_11 = Instance_Hadoop('instance_11', InstanceType.HADOOP, host_4, instance_list)
    instance_12 = Instance_Hadoop('instance_12', InstanceType.HADOOP, host_4, instance_list)
    instance_13 = Instance_Hadoop('instance_13', InstanceType.HADOOP, host_4, instance_list)
    instance_14 = Instance_Hadoop('instance_14', InstanceType.HADOOP, host_4, instance_list)
    instance_15 = Instance_Hadoop('instance_15', InstanceType.HADOOP, host_4, instance_list)
    instance_16 = Instance_Hadoop('instance_16', InstanceType.HADOOP, host_4, instance_list)

    file_list_1 = [host_2, host_3]
    file_list_2 = [host_2, host_4]
    file_list_3 = [host_1, host_1]

    instance_1.setFileHostList(file_list_1)
    instance_2.setFileHostList(file_list_2)
    instance_3.setFileHostList(file_list_2)
    instance_4.setFileHostList(file_list_3)
    instance_5.setFileHostList(file_list_2)
    instance_6.setFileHostList(file_list_1)
    instance_7.setFileHostList(file_list_3)
    instance_8.setFileHostList(file_list_3)
    instance_9.setFileHostList(file_list_1)
    instance_10.setFileHostList(file_list_1)
    instance_11.setFileHostList(file_list_2)
    instance_12.setFileHostList(file_list_3)
    instance_13.setFileHostList(file_list_2)
    instance_14.setFileHostList(file_list_2)
    instance_15.setFileHostList(file_list_1)
    instance_16.setFileHostList(file_list_3)

def setup_environment_4():
    host_1 = Host_Hadoop('host_1', host_list)
    host_2 = Host_Hadoop('host_2', host_list)
    host_3 = Host_Hadoop('host_3', host_list)
    host_4 = Host_Hadoop('host_4', host_list)

    host_1.addFile('file1')
    host_1.addFile('file5')
    host_2.addFile('file2')
    host_2.addFile('file6')
    host_3.addFile('file3')
    host_3.addFile('file7')
    host_4.addFile('file4')
    host_4.addFile('file8')

    instance_1 = Instance_Game_1('instance_1', InstanceType.GAME_1, host_1, instance_list)
    instance_2 = Instance_Game_1('instance_2', InstanceType.GAME_1, host_1, instance_list)
    instance_3 = Instance_Game_1('instance_3', InstanceType.GAME_1, host_1, instance_list)
    instance_4 = Instance_Game_1('instance_4', InstanceType.GAME_1, host_1, instance_list)
    instance_5 = Instance_Game_1('instance_5', InstanceType.GAME_1, host_1, instance_list)
    instance_6 = Instance_Game_1('instance_6', InstanceType.GAME_1, host_1, instance_list)
    instance_7 = Instance_Game_1('instance_7', InstanceType.GAME_1, host_2, instance_list)
    instance_8 = Instance_Game_1('instance_8', InstanceType.GAME_1, host_2, instance_list)
    instance_29 = Instance_Game_1('instance_29', InstanceType.GAME_1, host_1, instance_list)
    instance_30 = Instance_Game_1('instance_30', InstanceType.GAME_1, host_1, instance_list)
    instance_31 = Instance_Game_1('instance_31', InstanceType.GAME_1, host_3, instance_list)
    instance_32 = Instance_Game_1('instance_32', InstanceType.GAME_1, host_3, instance_list)


    instance_9 = Instance_Matlab_1('instance_9', InstanceType.MATLAB_1, host_1, instance_list)
    instance_10 = Instance_Matlab_1('instance_10', InstanceType.MATLAB_1, host_1, instance_list)
    instance_11 = Instance_Matlab_1('instance_11', InstanceType.MATLAB_1, host_4, instance_list)
    instance_12 = Instance_Matlab_1('instance_12', InstanceType.MATLAB_1, host_2, instance_list)
    instance_13 = Instance_Matlab_1('instance_13', InstanceType.MATLAB_1, host_1, instance_list)
    instance_14 = Instance_Matlab_1('instance_14', InstanceType.MATLAB_1, host_4, instance_list)
    instance_15 = Instance_Matlab_1('instance_15', InstanceType.MATLAB_1, host_3, instance_list)
    instance_16 = Instance_Matlab_1('instance_16', InstanceType.MATLAB_1_MASTER, host_3, instance_list)
    instance_33 = Instance_Matlab_1('instance_33', InstanceType.MATLAB_1, host_3, instance_list)
    instance_34 = Instance_Matlab_1('instance_34', InstanceType.MATLAB_1, host_1, instance_list)
    #instance_35 = Instance_Matlab_1('instance_35', InstanceType.MATLAB_1, host_4, instance_list)
    #instance_36 = Instance_Matlab_1('instance_36', InstanceType.MATLAB_1, host_4, instance_list)

    instance_17 = Instance_Hadoop('instance_17', InstanceType.HADOOP, host_1, instance_list)
    instance_18 = Instance_Hadoop('instance_18', InstanceType.HADOOP, host_1, instance_list)
    instance_19 = Instance_Hadoop('instance_19', InstanceType.HADOOP, host_2, instance_list)
    instance_20 = Instance_Hadoop('instance_20', InstanceType.HADOOP, host_2, instance_list)
    instance_21 = Instance_Hadoop('instance_21', InstanceType.HADOOP, host_2, instance_list)
    instance_22 = Instance_Hadoop('instance_22', InstanceType.HADOOP, host_3, instance_list)
    instance_23 = Instance_Hadoop('instance_23', InstanceType.HADOOP, host_3, instance_list)
    instance_24 = Instance_Hadoop('instance_24', InstanceType.HADOOP, host_3, instance_list)
    instance_25 = Instance_Hadoop('instance_25', InstanceType.HADOOP, host_1, instance_list)
    instance_26 = Instance_Hadoop('instance_26', InstanceType.HADOOP, host_4, instance_list)
    instance_27 = Instance_Hadoop('instance_27', InstanceType.HADOOP, host_3, instance_list)
    instance_28 = Instance_Hadoop('instance_28', InstanceType.HADOOP, host_3, instance_list)


    file_list_1 = [host_1, host_1]
    file_list_2 = [host_2, host_2]
    file_list_3 = [host_3, host_3]
    file_list_4 = [host_4, host_4]

    instance_17.setFileHostList(file_list_1)
    instance_18.setFileHostList(file_list_1)
    instance_19.setFileHostList(file_list_2)
    instance_20.setFileHostList(file_list_2)
    instance_21.setFileHostList(file_list_3)
    instance_22.setFileHostList(file_list_3)
    instance_23.setFileHostList(file_list_4)
    instance_24.setFileHostList(file_list_4)
    instance_25.setFileHostList(file_list_2)
    instance_26.setFileHostList(file_list_1)
    instance_27.setFileHostList(file_list_3)
    instance_28.setFileHostList(file_list_3)


############################################ WEBSOCKET ############################################
class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message('Welcome to WebSocket')

        thread = DataPusher(self)
        thread.start()


class DataPusher(threading.Thread):

    def __init__(self, socketHandler):
        super(DataPusher, self).__init__()
        self.socketHandler = socketHandler
        self.sshTool = Ssh_tool("114.212.189.134", 22, "root", "njuics08")

        self.count = 0

    def pushGmetric(self, name, value, host):
        cmd = "gmetric --name %s  --value %d --type uint32 --spoof %s" % (name, value, host)
        print cmd
        self.sshTool.remote_cmd(cmd)

    def pushEvent(self, type, info):
        self.socketHandler.write_message()

    def run(self):
        setup_environment_4()
        while True:
            #self.socketHandler.write_message("hello" + str(self.count))

            bandwidth1 = host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)
            bandwidth2 = host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)
            bandwidth3 = host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)
            bandwidth4 = host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, self.count, 1)

            distance_matlab = getMatlabDistance(instance_list)
            distance_hadoop = getHadoopDistance(instance_list)

            print str(bandwidth1)

            self.pushGmetric("bandwidth", bandwidth1, "10.0.0.1:host1")
            self.pushGmetric("bandwidth", bandwidth2, "10.0.0.2:host2")
            self.pushGmetric("bandwidth", bandwidth3, "10.0.0.3:host3")
            self.pushGmetric("bandwidth", bandwidth4, "10.0.0.4:host4")

            #self.pushGmetric("communication_cost_matlab", distance_matlab)
            #self.pushGmetric("communication_cost_hadoop", distance_hadoop)


            #display(host_list)

            if self.count > 4:
                final_game(2, self.socketHandler, self.count, host_list)
                final_hadoop(2, self.socketHandler, self.count, host_list, instance_list)
                final_matlab(2, self.socketHandler, self.count, host_list, instance_list)

            self.count += 1
            #time_count += 1
            #display(host_list)
            time.sleep(3)


if __name__ == '__main__':

    ####################################### experiment-1 #######################################
    if exp == 1:
        setup_environment_1()
        display(host_list)

        host1_cpuUtil = []
        host2_cpuUtil = []
        host3_cpuUtil = []
        host4_cpuUtil = []
        total_distance = []
        time = []

        while time_count < 80:
            host1_cpuUtil.append(host_list['host_1'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host2_cpuUtil.append(host_list['host_2'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host3_cpuUtil.append(host_list['host_3'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host4_cpuUtil.append(host_list['host_4'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            total_distance.append(getTotalDistance(instance_list))
            time.append(time_count)
            if time_count > 10:
                matlab_1_consolidate_comparison(8, time_count, host_list)
            time_count += 1
        display(host_list)


        setup_environment_1()
        time_count = 0
        display(host_list)

        host1_cpuUtil_1 = []
        host2_cpuUtil_1 = []
        host3_cpuUtil_1 = []
        host4_cpuUtil_1 = []
        total_distance_1 = []
        time_1 = []

        while time_count < 80:
            host1_cpuUtil_1.append(host_list['host_1'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host2_cpuUtil_1.append(host_list['host_2'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host3_cpuUtil_1.append(host_list['host_3'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host4_cpuUtil_1.append(host_list['host_4'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            total_distance_1.append(getTotalDistance(instance_list))
            time_1.append(time_count)
            if time_count > 10:
                matlab_1_consolidate(4, time_count, host_list)
                matlab_2_consolidate(4, time_count, host_list)
            time_count += 1
        display(host_list)

        plt.subplot(211)
        plt.plot(time, host1_cpuUtil, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_cpuUtil, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_cpuUtil, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_cpuUtil, label = 'host-4', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('cpu_util(%)')
        plt.legend()
        plt.grid(True)

        plt.subplot(212)
        plt.plot(time, host1_cpuUtil_1, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_cpuUtil_1, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_cpuUtil_1, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_cpuUtil_1, label = 'host-4', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('cpu_util(%)')
        plt.legend()
        plt.grid(True)

        plt.subplot(313)
        plt.plot(time, total_distance, label = 'MM', linewidth = 2)
        plt.plot(time, total_distance_1, label = 'Rule-Based', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('total_distance')
        plt.axis([20, 80, 0, 70])
        plt.legend()
        plt.grid(True)

        plt.show()


    ####################################### experiment-2 #######################################
    if exp == 2:
        setup_environment_2()

        display(host_list)
        host1_bandwidth = []
        host2_bandwidth = []
        host3_bandwidth = []
        host4_bandwidth = []
        time = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time.append(time_count)
            if time_count > 23:
                game_1_guarantee_qos_old(1, time_count, host_list)
                storage_1_consolidation_old(2, time_count, host_list)
            time_count += 1
        display(host_list)

        plt.subplot(211)
        plt.plot(time, host1_bandwidth, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_bandwidth, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_bandwidth, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_bandwidth, label = 'host-4', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('bandwidth(MHZ)')
        plt.grid(True)
        plt.legend()

        setup_environment_2()
        time_count = 0

        display(host_list)
        host1_bandwidth_1 = []
        host2_bandwidth_1 = []
        host3_bandwidth_1 = []
        host4_bandwidth_1 = []
        time_1 = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth_1.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth_1.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth_1.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth_1.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time_1.append(time_count)
            if time_count > 23:
                game_1_guarantee_qos(1, time_count, host_list)
                storage_1_consolidation(2, time_count, host_list)
            time_count += 1
        display(host_list)

        plt.subplot(212)
        plt.plot(time_1, host1_bandwidth_1, label = 'host-1', linewidth = 2)
        plt.plot(time_1, host2_bandwidth_1, label = 'host-2', linewidth = 2)
        plt.plot(time_1, host3_bandwidth_1, label = 'host-3', linewidth = 2)
        plt.plot(time_1, host4_bandwidth_1, label = 'host-4', linewidth = 2)
        plt.xlabel('time(h)')
        plt.ylabel('bandwidth(MHZ)')
        plt.grid(True)
        plt.legend()


        #print game_migration

        #x, y = getStatus(game_migration)
        #game_migration_1 = [24, 28, 38]
        #x1, y1 = getStatus(game_migration_1)
        #x1.append(60)
        #y1.append(10)
        #
        #
        #plt.subplot(413)
        #plt.plot(x, y, label = 'game_server', linewidth = 2, color = 'red')
        #plt.axis([20, 60, -5, 15])
        #plt.xlabel('time(h)')
        #plt.ylabel('status')
        #plt.yticks(range(-5, 15, 5), ['', 'down', '', 'running', ''])
        #plt.grid(True)
        #plt.legend()
        #
        #plt.subplot(414)
        #plt.plot(x1, y1, label = 'game_server', linewidth = 2, color = 'red')
        #plt.axis([20, 60, -5, 15])
        #plt.xlabel('time(h)')
        #plt.ylabel('status')
        #plt.yticks(range(-5, 15, 5), ['', 'down', '', 'running', ''])
        #plt.grid(True)
        #plt.legend()

        plt.show()


    ####################################### experiment-3 #######################################
    if exp == 3:
        setup_environment_3()
        display(host_list)

        totalDistance = []
        time = []

        tmpInstance = []
        for instanceId in instance_list:
            tmpInstance.append(instanceId)

        while time_count < 30:
            if time_count == 10:
                display(host_list)
                host_list_1 = [host_list['host_2'], host_list['host_3']]
                host_list_2 = [host_list['host_2'], host_list['host_1']]
                host_list_3 = [host_list['host_4'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_3)
                instance_list['instance_3'].setFileHostList(host_list_3)
                instance_list['instance_4'].setFileHostList(host_list_2)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_3)
                instance_list['instance_11'].setFileHostList(host_list_3)
                instance_list['instance_12'].setFileHostList(host_list_1)
                instance_list['instance_13'].setFileHostList(host_list_3)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            if time_count == 20:
                display(host_list)
                host_list_1 = [host_list['host_4'], host_list['host_4']]
                host_list_2 = [host_list['host_1'], host_list['host_3']]
                host_list_3 = [host_list['host_3'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_2)
                instance_list['instance_3'].setFileHostList(host_list_1)
                instance_list['instance_4'].setFileHostList(host_list_1)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_2)
                instance_list['instance_11'].setFileHostList(host_list_2)
                instance_list['instance_12'].setFileHostList(host_list_3)
                instance_list['instance_13'].setFileHostList(host_list_1)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            totalDistance.append(getTotalFileDistance(instance_list))
            time.append(time_count)

            hadoop_consolidation(2, time_count, host_list, instance_list, tmpInstance)
            time_count += 1
        display(host_list)

        setup_environment_3()
        #display(host_list)
        time_count = 0

        totalDistance_1 = []
        time_1 = []

        while time_count < 30:
            if time_count == 10:
                display(host_list)
                host_list_1 = [host_list['host_2'], host_list['host_3']]
                host_list_2 = [host_list['host_2'], host_list['host_1']]
                host_list_3 = [host_list['host_4'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_3)
                instance_list['instance_3'].setFileHostList(host_list_3)
                instance_list['instance_4'].setFileHostList(host_list_2)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_3)
                instance_list['instance_11'].setFileHostList(host_list_3)
                instance_list['instance_12'].setFileHostList(host_list_1)
                instance_list['instance_13'].setFileHostList(host_list_3)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            if time_count == 20:
                display(host_list)
                host_list_1 = [host_list['host_4'], host_list['host_4']]
                host_list_2 = [host_list['host_1'], host_list['host_3']]
                host_list_3 = [host_list['host_3'], host_list['host_4']]

                instance_list['instance_1'].setFileHostList(host_list_1)
                instance_list['instance_2'].setFileHostList(host_list_2)
                instance_list['instance_3'].setFileHostList(host_list_1)
                instance_list['instance_4'].setFileHostList(host_list_1)
                instance_list['instance_5'].setFileHostList(host_list_3)
                instance_list['instance_6'].setFileHostList(host_list_3)
                instance_list['instance_7'].setFileHostList(host_list_2)
                instance_list['instance_8'].setFileHostList(host_list_1)
                instance_list['instance_9'].setFileHostList(host_list_2)
                instance_list['instance_10'].setFileHostList(host_list_2)
                instance_list['instance_11'].setFileHostList(host_list_2)
                instance_list['instance_12'].setFileHostList(host_list_3)
                instance_list['instance_13'].setFileHostList(host_list_1)
                instance_list['instance_14'].setFileHostList(host_list_2)
                instance_list['instance_15'].setFileHostList(host_list_2)
                instance_list['instance_16'].setFileHostList(host_list_3)

                for instanceId in instance_list:
                    tmpInstance.append(instanceId)

            totalDistance_1.append(getTotalFileDistance(instance_list))
            time_1.append(time_count)

            hadoop_consolidation_old(2, time_count, host_list)
            time_count += 1
        #display(host_list)

        plt.plot(time, totalDistance_1, label = 'MM', marker = 's', linewidth = 2, color = 'orange')
        plt.plot(time_1, totalDistance, label = 'Rule-based', marker = 'v', linewidth = 2, color = 'blue')
        plt.xlabel('time(h)')
        plt.ylabel('total_distance')
        plt.axis([0, 30, 0, 110])
        plt.grid(True)
        plt.legend()
        plt.show()

    if exp == 4:
        setup_environment_4()

        display(host_list)
        host1_cpuUtil = []
        host2_cpuUtil = []
        host3_cpuUtil = []
        host4_cpuUtil = []

        host1_bandwidth = []
        host2_bandwidth = []
        host3_bandwidth = []
        host4_bandwidth = []
        distance_matlab = []
        distance_hadoop = []
        time = []
        while time_count < 80:

            host1_cpuUtil.append(host_list['host_1'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host2_cpuUtil.append(host_list['host_2'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host3_cpuUtil.append(host_list['host_3'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))
            host4_cpuUtil.append(host_list['host_4'].getStatisticData('history', ResourceType.CPU_UTIL, time_count, 1))

            #plot the host bandwidth pic
            host1_bandwidth.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time.append(time_count)
            distance_matlab.append(getMatlabDistance(instance_list))
            distance_hadoop.append(getHadoopDistance(instance_list))
            if time_count > 23:
                final_game_1(2, time_count, host_list)
                final_hadoop_1(2, time_count, host_list, instance_list)
                final_matlab_1(2, time_count, host_list, instance_list)
            time_count += 1
        display(host_list)

        setup_environment_4()
        time_count = 0

        display(host_list)

        host1_bandwidth_1 = []
        host2_bandwidth_1 = []
        host3_bandwidth_1 = []
        host4_bandwidth_1 = []
        distance_matlab_1 = []
        distance_hadoop_1 = []
        time_1 = []
        while time_count < 80:
            #plot the host bandwidth pic
            host1_bandwidth_1.append(host_list['host_1'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host2_bandwidth_1.append(host_list['host_2'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host3_bandwidth_1.append(host_list['host_3'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            host4_bandwidth_1.append(host_list['host_4'].getStatisticData('history', ResourceType.BANDWIDTH, time_count, 1))
            time_1.append(time_count)
            distance_matlab_1.append(getMatlabDistance(instance_list))
            distance_hadoop_1.append(getHadoopDistance(instance_list))
            if time_count > 23:
                final_game_old(2, time_count, host_list)
                final_consolidation(4, time_count, host_list)
            time_count += 1
        display(host_list)

        plt.subplot(411)
        plt.plot(time, host1_bandwidth, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_bandwidth, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_bandwidth, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_bandwidth, label = 'host-4', linewidth = 2)

        plt.xlabel('time(h)')
        plt.ylabel('bandwidth(MHZ)')
        plt.legend()
        plt.grid(True)

        plt.subplot(412)
        plt.plot(time, host1_bandwidth_1, label = 'host-1', linewidth = 2)
        plt.plot(time, host2_bandwidth_1, label = 'host-2', linewidth = 2)
        plt.plot(time, host3_bandwidth_1, label = 'host-3', linewidth = 2)
        plt.plot(time, host4_bandwidth_1, label = 'host-4', linewidth = 2)

        plt.xlabel('time(h)')
        plt.ylabel('bandwidth(MHZ)')
        plt.legend()
        plt.grid(True)


        plt.subplot(413)
        plt.plot(time, distance_matlab, label = 'Rule-based', linewidth = 2, color = 'orange', marker = 's')
        plt.plot(time, distance_matlab_1, label = 'MM', linewidth = 2, color = 'blue', marker = 'v')
        plt.xlabel('time(h)')
        plt.ylabel('communication_cost')
        plt.axis([20, 50, 0, 30])
        plt.legend()
        plt.grid(True)

        plt.subplot(414)
        plt.plot(time, distance_hadoop, label = 'Rule-based', linewidth = 2, color = 'orange', marker = 's')
        plt.plot(time, distance_hadoop_1, label = 'MM', linewidth = 2, color = 'blue', marker = 'v')
        plt.xlabel('time(h)')
        plt.ylabel('communication_cost')
        plt.axis([20, 50, 0, 50])
        plt.legend()
        plt.grid(True)

        plt.show()

    if exp == 5:
        app = tornado.web.Application([
        ('/soc', SocketHandler)
        ])

        app.listen(9008)
        tornado.ioloop.IOLoop.instance().start()

