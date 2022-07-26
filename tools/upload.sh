#!/bin/zsh

local_path=~/pycharmprojects/qqpixivbot
# shellcheck disable=SC2088
remote_path="~/ayaki"
remote_username="hakubill"
remote_host="bill.debian"

scp ${local_path}/main.py ${remote_username}@${remote_host}:${remote_path}
scp ${local_path}/features.py ${remote_username}@${remote_host}:${remote_path}
scp ${local_path}/config.yaml ${remote_username}@${remote_host}:${remote_path}
scp ${local_path}/private_config.yaml ${remote_username}@${remote_host}:${remote_path}