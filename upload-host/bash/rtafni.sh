#!/bin/bash

AFNI_PORT=7961

export LOG_DIR=/local/rtafni/brik
export AFNI_NOSPLASH=yes
export AFNI_REALTIME_Registration=3D:_realtime
export AFNI_REALTIME_Graph=Realtime
export AFNI_REALTIME_Verbose=No
export AFNI_TRUSTHOST=localhost
export AFNI_LAYOUT_FILE=${HOME}/.afni_layout
mkdir -p "${LOG_DIR}"

start_afni() {
    date >> $LOG_DIR/start_afni

    LOGFILE=$LOG_DIR/afni.log

    cd $LOG_DIR
    netstat -ltn |grep :${AFNI_PORT} || $AFNI_PLUGINPATH/afni -rt &>> $LOGFILE &

    count=0
    result=`netstat -ltn |grep :${AFNI_PORT}`
    while [ "$result" == "" ]; do
        echo "Waiting for port bondage..." >> $LOGFILE
        sleep 1
        result=`netstat -ltn |grep :${AFNI_PORT}`
        count=$(($count+1))
        if [[ $count -gt 20 ]]; then
          echo "Timeout!" >> $LOGFILE
          exit 1
        fi
    done
    sleep 1 # Give it just a moment to finish its startup...
}


start_dimon() {
    cd $1
    date >> $LOG_DIR/dimon_start
    $AFNI_PLUGINPATH/Dimon -infile_pattern '*' -rt -dicom_org -num_slices $2 -nt $3 -host 127.0.0.1 -quit \
      -rt_cmd "GRAPH_XRANGE $3" -rt_cmd 'GRAPH_YRANGE 2.0' \
      -drive_wait 'CLOSE_WINDOW sagittalimage' \
      -drive_wait 'CLOSE_WINDOW sagittalgraph' &> $LOG_DIR/Dimon.log
    cd ..
}


rm $LOG_DIR/*

echo $0 $* > $LOG_DIR/command_list

start_afni
start_dimon $1 $2 $3