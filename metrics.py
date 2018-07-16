#!/usr/bin/python

import json
import psutil
import socket
import time
import os

def writemetric(metric_name, value):
    print("system_metrics,hostname="+ socket.gethostname() +",metric=" + metric_name + " value="+ str(value) +" "+ str(int(time.time()*1000000000)))


if __name__ == '__main__':
    cpu = psutil.cpu_times_percent()
    disk_root = psutil.disk_usage('/')
    vmem = psutil.virtual_memory()
    smem = psutil.swap_memory()

    # Disk space
    writemetric("disk.percent./", disk_root.percent)

    # Memory
    writemetric("mem.total", vmem.total)
    writemetric("mem.available", vmem.available)
    writemetric("mem.used", vmem.used)
    writemetric("mem.free", vmem.free)
    writemetric("mem.buffers", vmem.buffers)
    writemetric("mem.cached", vmem.cached)

    # Swap
    writemetric("swap.total", smem.total)
    writemetric("swap.used", smem.used)
    writemetric("swap.free", smem.free)
    writemetric("swap.percent", smem.percent)

    # CPU Load
    load = os.getloadavg()
    result = "%f %f %f" % load
    loadstring = result.split()

    writemetric("cpu.load1", float(loadstring[0]))
    writemetric("cpu.load5", float(loadstring[1]))
    writemetric("cpu.load15", float(loadstring[2]))

    # Networking
    nics = psutil.net_io_counters(pernic=True)
    for nic in nics:
        (bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout) = nics[nic]

        # Ignore inactive network interfaces
        if packets_recv != 0 and packets_sent != 0 and 'veth' not in nic and 'docker' not in nic:
            writemetric(nic + ".bytes_sent", bytes_sent)
            writemetric(nic + ".bytes_recv", bytes_recv)


    # Disk IO
    diskio = psutil.disk_io_counters(perdisk=True)
    for disk in diskio:
        if len(diskio[disk]) == 6:
            (read_count, write_count, read_bytes, write_bytes, read_time, write_time) = diskio[disk]
        else:
            (read_count, write_count, read_bytes, write_bytes, read_time, write_time, read_merged_count, write_merged_count, busy_time) = diskio[disk]
            writemetric(disk + ".busy_time", busy_time)

        writemetric(disk + ".read_bytes", read_bytes)
        writemetric(disk + ".write_bytes", write_bytes)
        writemetric(disk + ".read_time", read_time)
        writemetric(disk + ".write_time", write_time)

