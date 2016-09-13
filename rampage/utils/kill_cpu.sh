#!/bin/bash

secs=$1
num_cpu=`grep processor /proc/cpuinfo  | wc -l`
if [ "$#" -eq 2 ]; then
    num_cpu=$2
fi

for i in `seq 1 $num_cpu`; do
    {
        while :
        do
            if [ "$SECONDS" -ge "$secs" ]
            then
                exit
            fi
        done
    }&
done