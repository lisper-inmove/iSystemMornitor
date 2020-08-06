# -*- coding: utf-8 -*-

import time
import psutil

from date_utils import DateUtils
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
        self.print()
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
        pass

    def print(self):
        dateutil_obj = DateUtils()
        for cpu_time in self.cpu_times_proto.cpu_times:
            print("CPU Index: {}".format(cpu_time.cpu_index))
            print("统计时间: {}".format(dateutil_obj.timestamp_to_string(cpu_time.timestamp)))
            print("用户进程耗时: {}(秒)".format(cpu_time.user_mode_time))
            print("内核进程耗时: {}(秒)".format(cpu_time.kernel_mode_time))
            print("CPU空闲时间: {}(秒)".format(cpu_time.idle_time))


if __name__ == '__main__':
    obj = CPUMonitor()
    obj.collect()
