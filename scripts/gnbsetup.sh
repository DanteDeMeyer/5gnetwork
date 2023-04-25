#!/bin/bash

while true
do
    cd ~/openairinterface5g/cmake_targets/ran_build/build
    sudo ./nr-softmodem -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf --sa -E --continuous-tx
    sleep 2
done
