#!/bin/bash

echo_and_log()
{
  message=$1
  echo $message
  echo "$(date '+%Y-%m-%d %H:%M:%S') | run.sh script |" $message >> roomBot.log
}


echo_and_log "Starting bot"
python -u run.py
result=$?

time_start=$(($(date +%s%N)/1000000))
while [ ${result} = 1 ]; do
    echo_and_log "Got exit code 1"
    echo_and_log "Restarting bot"
    
    python -u run.py
    result=$?
    time_finished=$(($(date +%s%N)/1000000))

    if [ `expr ${time_finished} - ${time_start}` -lt 30000 ]; then
        echo_and_log "restart in less than 30 seconds. exit"
        
        break
    fi
    
    time_start=${time_finished}
done


echo_and_log "Bot exited with code ${result}"
exit $result
