#!/bin/bash

# 启动网站
/usr/local/python3/bin/uwsgi --emperor /etc/uwsgi/vassals --uid root --gid root --daemonize /var/log/uwsgi-emperor.log