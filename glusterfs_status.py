#!/usr/bin/env python2

from __future__ import print_function
import subprocess
import argparse
import socket
import sys


GLUSTER_POOL_LIST = '/sbin/gluster pool list'
GLUSTER_VOLUME_STATUS = '/sbin/gluster volume status'


def get_output(command):
    try:
        return subprocess.check_output(command.split())
    except (
        subprocess.CalledProcessError,
        OSError,
    ) as e:
        print_error(e)


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_number_of_connected_peers():
    stdout = get_output(GLUSTER_POOL_LIST)
    if stdout:
        connected_pool_list = [line for line in stdout.splitlines() if 'Connected' in line]
        return len(connected_pool_list)
    return 0


def count_online_bricks(volume):
    stdout = get_output('{} {} detail'.format(GLUSTER_VOLUME_STATUS, volume))
    if stdout:
        online_statuses = [line.split()[-1] for line in stdout.splitlines() if 'Online' in line]
        return online_statuses.count('Y')
    return 0


def check_mount_status(volume):
    try:
        with open('/proc/mounts') as f:
            if 'localhost:/{}'.format(volume) in f.read():
                return 1
    except IOError as e:
        print_error(e)

    return 0


def print_metrics(volume):
    print(
        'glusterfs_status,'
        'host={host},'
        'volume={volume} '
        'connected_peers={connected_peers},'
        'online_bricks={online_bricks},'
        'is_mounted={is_mounted}'.format(
            host=socket.gethostname(),
            volume=volume,
            connected_peers=get_number_of_connected_peers(),
            online_bricks=count_online_bricks(volume),
            is_mounted=check_mount_status(volume),
        )
    )


def parse_args():
    parser = argparse.ArgumentParser(description='Telegraf plugin to collect Glusterfs metrics (Influxdb format)')
    parser.add_argument('volumes', help='space separated Glusterfs volumes', nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    for volume in parse_args().volumes:
        print_metrics(volume)

