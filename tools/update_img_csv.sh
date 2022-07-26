#!/bin/zsh
# for bill.debian
# hosts: 192.168.2.132 bill.debian

# 0 - stop remote program
# 1 - fetch remote csv
scp hakubill@bill.debian:~/ayaki/pixiv_src.csv ~/pycharmprojects/qqpixivbot/
# 2 - backup remote csv
# 3 - run python script
cd ~/pycharmprojects/qqpixivbot && cp pixiv_src.csv pixiv_src.bak
python3 upload.py
# 4 - check new csv manually
# 5 - backup new csv
# 6 - push to remote
cp pixiv_src.csv pixiv_src.bak
scp pixiv_src.csv hakubill@bill.debian:~/ayaki
# 7 - start remote program