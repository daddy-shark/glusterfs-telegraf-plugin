# Telegraf plugin to collect GlusterFS metrics

This simple python script should be used via telegraf exec input plugin with influx format. It collects the following GlusterFS metrics:
- Number of connected peers (`gluster pool list`)
- Number of online bricks for each volume (`gluster volume status <volume> detail`)
- Mount status for each volume (by local `/proc/mounts`)

## Usage

See usage with:
```
glusterfs_status.py -h
```

Usage example:
```
sudo /usr/local/bin/glusterfs_status.py vol1 vol2
glusterfs_status,host=example_host.com,volume=vol1 connected_peers=3,online_bricks=3,is_mounted=1
glusterfs_status,host=example_host.com,volume=vol2 connected_peers=3,online_bricks=3,is_mounted=1
```

## Installation
Download script:
```
wget -O /usr/local/bin/glusterfs_status.py https://raw.githubusercontent.com/sharkman-devops/glusterfs-telegraf-plugin/master/glusterfs_status.py
```
Make it executable:
```
chmod +x /usr/local/bin/glusterfs_status.py
```
Add permitions to execute it via sudo:
```
echo 'telegraf ALL = NOPASSWD: /usr/local/bin/glusterfs_status.py' > /etc/sudoers.d/glusterfs_telegraf_sudoers
```
Configure telegraf:
```
cat <<EOT > /etc/telegraf/telegraf.d/glusterfs_status.conf
[[inputs.exec]]
  command = "sudo /usr/local/bin/glusterfs_status.py vol1 vol2"
  timeout = "10s"
  data_format = "influx"
  interval = "60s"
EOT
```
Please don't forget to replace `vol1` and `vol2` to correct volumes names!

