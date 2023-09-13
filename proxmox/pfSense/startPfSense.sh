#!/bin/bash

sleep 5
systemctl stop pve-cluster
pmxcfs -l
qm start 102
sleep 5
killall pmxcfs
systemctl start pve-cluster
