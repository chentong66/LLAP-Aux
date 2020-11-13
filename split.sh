#!/bin/bash
afile=$1'alog.txt'
vfile=$1'vlog.txt'
atime=$1'alog-time.txt'
appg=$1'alog-ppg.txt'
vtime=$1'vlog-time.txt'
vppg=$1'vlog-ppg.txt'
awk -F',' '{print $1}' $afile > $appg
awk -F',' '{print $2}' $afile > $atime
awk -F',' '{print $1}' $vfile > $vppg
awk -F',' '{print $2}' $vfile > $vtime
