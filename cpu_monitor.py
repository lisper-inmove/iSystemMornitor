# -*- coding: utf-8 -*-

import time
import psutil

import proto.cpu_monitor_pb2 as cpu_monitor_pb

class CPUMonitor:
    def __init__(self):
        pass

    def init(self):
        self.cpu_times_proto = cpu_monitor_pb.CPUTimes()
        self.cpu_utilizations_proto = cpu_monitor_pb.CPUUtilizations()

    def collect(self):
        self.init()
        self.cpu_times()
        self.cpu_utilizations()
        self.save()

    def cpu_times(self):
        cpu_times = psutil.cpu_times(percpu=True)
        for index, cpu_time in enumerate(cpu_times):
            cpu_time_proto = self.cpu_times_proto.cpu_times.add()
            cpu_time_proto.cpu_index = index + 1
            cpu_time_proto.timestamp = int(time.time())
            cpu_time_proto.user_mode_time = cpu_time.user
            cpu_time_proto.kernel_mode_time = cpu_time.system
            cpu_time_proto.idle_time = cpu_time.idle

    def cpu_utilizations(self):
        cpu_utilizations = psutil.cpu_percent(percpu=True)
        for index, cpu_utilization in enumerate(cpu_utilizations):
            cpu_utilization_proto = self.cpu_utilizations_proto.cpu_utilizations.add()
            cpu_utilization_proto.timestamp = int(time.time())
            cpu_utilization_proto.cpu_index = index + 1
            cpu_utilization_proto.percent = cpu_utilization

    def save(self):
        print("保存数据到数据库")
        print(self.cpu_times_proto)
        print(self.cpu_utilizations_proto)

if __name__ == '__main__':
    obj = CPUMonitor()
    obj.collect()
