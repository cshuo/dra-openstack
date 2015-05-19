__author__ = 'pike'

import json

from Filter import *
from Rank import *
from Util import *


#migration time
game_migration = []
storage_migration = []

############################################### migrate ###############################################
def migrate_instance(srcHost, destHost, instance):
        if not instance:
            print 'no instance to migrate'
            return
        if srcHost == None:
            print 'no srcHost'
            return
        if destHost == None:
            print 'no destHost'
            return

        if srcHost.getId() == destHost.getId():
            return

        if srcHost == None or destHost == None:
            print 'no host to migrate'
            return

        srcHost.removeInstance(instance)
        destHost.addInstance(instance)
        instance.setHost(destHost)
        print '%s\t==>\t%s\t==>\t%s' % (srcHost.id, instance.getId(), destHost.getId())

        #if instance.getType() == InstanceType.GAME_1:
        #    global game_migration_num
        #    game_migration.append(time_count)
        #if instance.getType() == InstanceType.STORAGE_1:
        #    global storage_migration_num
        #    storage_migration.append(time_count)



############################################### worker ###############################################

def matlab_1_consolidate(period, time_count, host_list):
    if (time_count % period == 0):
        #srcHost = select_host_min_instance(host_list, InstanceType.MATLAB_1)
        #migrateInstance = select_instance_random(srcHost, InstanceType.MATLAB_1)
        #destHost = select_host_max_instance(host_list, InstanceType.MATLAB_1)
        #migrate_instance(srcHost, destHost, migrateInstance)
        src_host_list = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, False)
        src_host_list = filter_host_instanceType(src_host_list, InstanceType.MATLAB_1, True)
        #srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        srcHost = select_host_random(src_host_list)

        migrateInstance = select_instance_random(srcHost, InstanceType.MATLAB_1)

        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)

        migrate_instance(srcHost, destHost, migrateInstance)

def matlab_2_consolidate(period, time_count, host_list):
    if (time_count % period == 0):
        src_host_list = filter_host_instanceType(host_list, InstanceType.MATLAB_2_MASTER, False)
        src_host_list = filter_host_instanceType(src_host_list, InstanceType.MATLAB_2, True)
        #srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        srcHost = select_host_random(src_host_list)

        migrateInstance = select_instance_random(srcHost, InstanceType.MATLAB_2)

        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_2_MASTER, True)[0]
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)

        migrate_instance(srcHost, destHost, migrateInstance)

def matlab_1_consolidate_comparison(period, time_count, host_list):
    if (time_count % period == 0):
        src_host_list = filter_host_instanceType(host_list, InstanceType.ALL, True)
        srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_max_cpu(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)

def matlab_2_consolidate_comparison(period, time_count, host_list):
    if (time_count % period == 0):
        src_host_list = filter_host_instanceType(host_list, InstanceType.ALL, True)
        srcHost = select_host_min_cpu(src_host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_max_cpu(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)

def game_1_guarantee_qos(period, time_count, host_list):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                migrateInstance = select_instance_random(host, InstanceType.STORAGE_1)
                destHost = select_host_random(filter_host_instanceType(host_list, InstanceType.GAME_1, False))
                migrate_instance(srcHost, destHost, migrateInstance)

def storage_1_consolidation(period, time_count, host_list):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) < 600:
                srcHost = select_host_random(filter_host_instanceType(host_list, InstanceType.GAME_1, False))
                migrateInstance = select_instance_random(srcHost, InstanceType.STORAGE_1)
                destHost = host
                migrate_instance(srcHost, destHost, migrateInstance)

def game_1_guarantee_qos_old(period, time_count, host_list):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                migrateInstance = select_instance_random(host, InstanceType.ALL)
                dest_host_list = filter_host_bandwidth(host_list, 'future', time_count, 2, 600)
                destHost = select_host_min_bandwidth(dest_host_list, 'future', time_count, 2)
                migrate_instance(srcHost, destHost, migrateInstance)

def storage_1_consolidation_old(period, time_count, host_list):
    if (time_count % period == 0):
        srcHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_bandwidth(host_list, 'future', time_count, 2, 600)
        destHost = select_host_max_bandwidth(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)

def hadoop_consolidation(period, time_count, host_list, instance_list, tmpInstance):
    if (time_count % period == 0):
        #for instanceId in instance_list:
        for i in range(4):
            if len(tmpInstance) == 0: break
            instanceId = tmpInstance.pop()
            instance = instance_list[instanceId]
            file_host_list = instance.getFileHostList()

            #file_host1 = filter_host_containsFile(host_list, fileList[0], True)[0]
            #file_host2 = filter_host_containsFile(host_list, fileList[1], True)[0]

            #file_host_list = [file_host1, file_host2]

            #srcHostList = filter_host_instanceType(host_list, InstanceType.HADOOP, True)
            #srcHost = select_host_file_distance_max(file_host_list, srcHostList, host_distance_matrix)
            srcHost = instance.getHost()

            #migrateInstance = select_instance_random(srcHost, InstanceType.HADOOP)
            migrateInstance = instance

            srcHost.removeInstance(migrateInstance)

            destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
            destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)

            srcHost.addInstance(migrateInstance)

            #if srcHost.getInstanceNum(InstanceType.HADOOP) == 8:
            #    return

            migrate_instance(srcHost, destHost, migrateInstance)


def hadoop_consolidation_old(period, time_count, host_list):
    if (time_count % period == 0):
        srcHostList = filter_host_instanceType(host_list, InstanceType.HADOOP, True)
        srcHost = select_host_min_instance(srcHostList, InstanceType.HADOOP)

        migrateInstance = select_instance_random(srcHost, InstanceType.HADOOP)

        destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
        destHost = select_host_max_instance(destHostList, InstanceType.HADOOP)

        if srcHost.getInstanceNum(InstanceType.HADOOP) == 8:
            return

        migrate_instance(srcHost, destHost, migrateInstance)


def final_game(period, socket, time_count, host_list):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                socket.write_message(json.dumps({'type' : 'event', 'value' : '(host (id %s) (> bandwidth 700))' % host.getId()}))

                srcHost = host
                socket.write_message(json.dumps({'type' : 'action', 'value' : 'srcHost = %s' % host.getId()}))

                migrateInstance = select_instance_random_1(host, InstanceType.GAME_1, True)
                socket.write_message(json.dumps({'type' : 'action', 'value' : 'migrateInstance = %s' % migrateInstance.getId()}))

                destHost = None

                if migrateInstance.getType() == InstanceType.HADOOP:
                    socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s evacuate)' % migrateInstance.getId()}))
                    file_host_list = migrateInstance.getFileHostList()
                    destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))
                    destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min_file_distance'}))
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

                    if destHost == srcHost:
                        migrateInstance = select_instance_random(srcHost, InstanceType.GAME_1)
                        destHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)

                if migrateInstance.getType() == InstanceType.MATLAB_1:
                    socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s evacuate)' % migrateInstance.getId()}))
                    masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
                    dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))
                    destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min cpu distance'}))
                    socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

                migrate_instance(srcHost, destHost, migrateInstance)
                if srcHost != None and destHost != None and migrateInstance != None:
                    socket.write_message(json.dumps({'type' : 'action', 'value' : '%s ==> %s ==> %s' % (srcHost.getId(), migrateInstance.getId(), destHost.getId())}))
                socket.write_message(json.dumps(getHostsMapper(host_list)))

def final_hadoop(period, socket, time_count, host_list, instance_list):
    if (time_count % period == 0):
        instance = filter_instance_type(instance_list, InstanceType.HADOOP)
        socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s hadoop)' % instance.getId()}))
        srcHost = instance.getHost()
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'srcHost = %s' % srcHost.getId()}))

        file_host_list = instance.getFileHostList()
        destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))

        destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min_file_distance'}))
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

        if destHost.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700 or destHost.getInstanceNum(InstanceType.GAME_1) > 0:
            return
        migrate_instance(srcHost, destHost, instance)
        socket.write_message(json.dumps({'type' : 'action', 'value' : '%s ==> %s ==> %s' % (srcHost.getId(), instance.getId(), destHost.getId())}))
        socket.write_message(json.dumps({'type' : 'hosts', 'value' : getHostsMapper(host_list)}))

def final_matlab(period, socket, time_count, host_list, instance_list):
    if (time_count % period == 0):
        instance = filter_instance_type(instance_list, InstanceType.MATLAB_1)
        socket.write_message(json.dumps({'type' : 'event', 'value' : '(instance %s matlab)' % instance.getId()}))
        srcHost = instance.getHost()
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'srcHost = %s' % srcHost.getId()}))

        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'filter cpu_util'}))

        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'rank min cpu distance'}))
        socket.write_message(json.dumps({'type' : 'action', 'value' : 'destHost = %s' % destHost.getId()}))

        if destHost.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700 or destHost.getInstanceNum(InstanceType.GAME_1) > 0:
            return
        migrate_instance(srcHost, destHost, instance)
        socket.write_message(json.dumps({'type' : 'action', 'value' : '%s ==> %s ==> %s' % (srcHost.getId(), instance.getId(), destHost.getId())}))
        socket.write_message(json.dumps(getHostsMapper(host_list)))

def final_game_1(period, time_count, host_list):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                migrateInstance = select_instance_random_1(host, InstanceType.GAME_1, True)
                destHost = None

                if migrateInstance.getType() == InstanceType.HADOOP:
                    file_host_list = migrateInstance.getFileHostList()
                    destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)
                    destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)

                    if destHost == srcHost:
                        migrateInstance = select_instance_random(srcHost, InstanceType.GAME_1)
                        destHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)

                if migrateInstance.getType() == InstanceType.MATLAB_1:
                    masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]
                    dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
                    destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)

                migrate_instance(srcHost, destHost, migrateInstance)

def final_hadoop_1(period, time_count, host_list, instance_list):
    if (time_count % period == 0):
        instance = filter_instance_type(instance_list, InstanceType.HADOOP)
        srcHost = instance.getHost()

        file_host_list = instance.getFileHostList()
        destHostList = filter_host_instanceNum(host_list, 8, InstanceType.HADOOP)

        destHost = select_host_file_distance_min(file_host_list, destHostList, host_distance_matrix)

        if destHost.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700 or destHost.getInstanceNum(InstanceType.GAME_1) > 0:
            return
        migrate_instance(srcHost, destHost, instance)

def final_matlab_1(period, time_count, host_list, instance_list):
    if (time_count % period == 0):
        instance = filter_instance_type(instance_list, InstanceType.MATLAB_1)
        srcHost = instance.getHost()
        masterHost = filter_host_instanceType(host_list, InstanceType.MATLAB_1_MASTER, True)[0]

        dest_host_list = filter_host_cpu(host_list, 'future', time_count, 2, 80)
        destHost = select_host_cpu_distance(masterHost, dest_host_list, host_distance_matrix, 'future', time_count, 2)

        if destHost.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700 or destHost.getInstanceNum(InstanceType.GAME_1) > 0:
            return
        migrate_instance(srcHost, destHost, instance)

def final_game_old(period, time_count, host_list):
    if (time_count % period == 0):
        game_hostList = filter_host_instanceType(host_list, InstanceType.GAME_1, True)
        for host in game_hostList:
            if host.getStatisticData('future', ResourceType.BANDWIDTH, time_count, 2) > 700:
                srcHost = host
                #migrateInstance = select_instance_random_1(host, InstanceType.GAME_1, True)
                migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
                #destHost = select_host_random(filter_host_instanceType(host_list, InstanceType.GAME_1, False))
                destHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)
                migrate_instance(srcHost, destHost, migrateInstance)


def final_consolidation(period, time_count, host_list):
    if (time_count % period == 0):
        srcHost = select_host_min_bandwidth(host_list, 'future', time_count, 2)
        migrateInstance = select_instance_random(srcHost, InstanceType.ALL)
        dest_host_list = filter_host_bandwidth(host_list, 'future', time_count, 2, 600)
        destHost = select_host_max_bandwidth(dest_host_list, 'future', time_count, 2)
        migrate_instance(srcHost, destHost, migrateInstance)